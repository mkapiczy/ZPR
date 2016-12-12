from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import View

from student.models import StudentUser
from tutor.models import TutorUser
from .forms import UserForm, LoginForm
from .models import UserProfile, Course


class LoginView(View):
    form_class = LoginForm
    template_name = 'main/login_form.html'

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return redirect_according_to_user_type(request, user)
        else:
            form = self.form_class(None)
            return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None and user.is_active and user.is_authenticated:
            login(request, user)
            return redirect_according_to_user_type(request, user)
        else:
            return render(request, self.template_name, {'form': form, 'error_message': 'Credentials are incorrect'})


class LogoutView(View):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LogoutView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        logout(request)
        return redirect('main:login')


class UserFormView(View):
    form_class = UserForm
    template_name = 'main/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            is_tutor = user.is_tutor

            password = form.cleaned_data['password']
            username = user.first_name + ' ' + user.last_name

            user.username = username
            user.set_password(password)
            try:
                user.save()
                profile = createNewUserProfile(user)
                if is_tutor:
                    createNewTutorUser(profile)
                else:
                   createNewStudentUser(profile)
            except IntegrityError as e:
                return uniqueContraintValidationRedirect(self, request, form)

            user = authenticate(username=username, password=password)

            if user is not None and user.is_active:
                login(request, user)
                if is_tutor:
                    return redirect('tutor:index')
                else:
                    return redirect('student:index')

        return render(request, self.template_name, {'form': form})

def createNewUserProfile(user):
    profile = UserProfile()
    profile.user = user
    profile.username = user.username
    profile.first_name = user.first_name
    profile.last_name = user.last_name
    profile.save()
    return profile

def createNewTutorUser(profile):
    tutor = TutorUser()
    tutor.profile = profile
    tutor.save()

def createNewStudentUser(profile):
    student = StudentUser()
    student.profile = profile
    student.save()

def uniqueContraintValidationRedirect(self, request, form):
    return render(request, self.template_name, {'form': form, 'error_message': 'Istnieje już użytkownik o takich danych!'})

def redirect_according_to_user_type(request, user):
    user_profile = UserProfile.objects.get(user=user)
    if user_profile.is_student_user():
        return redirect('student:index')
    if user_profile.is_tutor_user():
        return redirect('tutor:index')
    else:
        return HttpResponseForbidden('User has no access rights for viewing this page')


def select_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    request.session['selected_course_id'] = course.id
    request.session['selected_course_shortname'] = course.short_name
    return redirect_according_to_user_type(request, request.user)
