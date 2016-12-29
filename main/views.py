from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View

from main.methods import createNewUserProfile, createNewTutorUser, createNewStudentUser, \
    uniqueContraintValidationRedirect
from .forms import UserForm


class LoginView(View):
    form_class = AuthenticationForm
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
