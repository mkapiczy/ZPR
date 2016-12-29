from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from main.models import UserProfile
from student.models import StudentUser
from tutor.models import TutorUser


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


def delayErrorAlertFade(request, alert):
    if (request.session.get('delayClearParam') is not None):
        request.session['delayClearParam'] = None
    else:
        request.session[alert] = None