import csv
import re
from io import TextIOWrapper
from sqlite3 import IntegrityError

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from main.methods import delayErrorAlertFade, setWrongFileSessionParam, isFileCorrect, createNewTutorUser
from main.models import MyUser, UserProfile
from main.permissions import has_tutor_permissions
from main.views import uniqueContraintValidationRedirect
from student.models import StudentUser
from tutor.models import TutorUser
from tutor_students.methods import addStudentToSelectedCourse, createNewStudentUser, createNewUserProfile, createMyUser, \
    createSystemUser, setNotAddedStudentsRequestParam, addTutorToSelectedCourse, removeTutorFromSelectedCourse
from tutor_tutors.forms import TutorForm


class TutorsView(View):
    template_name = 'tutor_tutors/tutors_index.html'
    index_template = 'tutor/index.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if has_tutor_permissions(request.user):
            return super(TutorsView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('User has no access rights for viewing this page')

    def get(self, request):
        delayErrorAlertFade(request,'notAddedStudents')
        selected_course_id = request.session.get('selected_course_id')
        if (selected_course_id is not None):
            course_tutors = TutorUser.objects.filter(courses__in=[selected_course_id])
            return render(request, self.template_name, {'nbar': 'tutors', 'course_tutors': course_tutors})
        else:
            return redirect('tutor:index')


class CreateTutor(View):
    form_class = TutorForm
    template_name = 'tutor_tutors/tutor_form.html'

    def get(self, request):
        form = TutorForm()
        return render(request, self.template_name, {'nbar': 'students', 'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            username = first_name + last_name
            try:
                profile = UserProfile.objects.get(username=username)
            except ObjectDoesNotExist:
                profile = None
            notAddedTutors = []
            if profile is not None:
                try:
                    tutor = TutorUser.objects.get(profile=profile)
                except ObjectDoesNotExist:
                    tutor = None
                if tutor is not None:
                    if not addTutorToSelectedCourse(tutor.id, request):
                        notAddedTutors.append(first_name + ' ' + last_name)
            else:
                try:
                    user = createSystemUser(first_name, last_name, password)
                    if (user is not None):
                        myUser = createMyUser(user)
                        profile = createNewUserProfile(myUser)
                        tutor =  createNewTutorUser(profile)
                        if (not addTutorToSelectedCourse(tutor.id, request)):
                            notAddedTutors.append(first_name + ' ' + last_name)
                except IntegrityError as e:
                    return uniqueContraintValidationRedirect(self, request, form)

            setNotAddedStudentsRequestParam(notAddedTutors, request)
            return redirect('tutor_tutors:index')


class DeleteTutor(View):
    def post(self, request, pk):
        tutor_id = request.POST['tutor_id']

        if tutor_id is not None:
            tutor = get_object_or_404(TutorUser, id=tutor_id)
            removeTutorFromSelectedCourse(tutor, request)
            if tutor.courses.all().count() == 0:
                profile = get_object_or_404(UserProfile, id=tutor.profile.id)
                myUser = get_object_or_404(MyUser, id=profile.user.id)
                user = get_object_or_404(User, id=myUser.user.id)

                try:
                    tutor.delete()
                    profile.delete()
                    myUser.delete()
                    user.delete()
                except User.DoesNotExist:
                    messages.error(request, "User does not exist")
                    return render(request, 'tutor_tutors/tutors_index.html', {'nbar': 'tutors'})

                except Exception as e:
                    return render(request, 'tutor_tutors/tutors_index.html', {'nbar': 'tutors', 'errors': e})

        return redirect('tutor_tutors:index')
