from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from main.models import MyUser, UserProfile, Course
from student.models import StudentUser


def setNotAddedStudentsRequestParam(notAddedStudents, request):
    request.session['delayClearParam'] = True
    request.session['notAddedStudents'] = notAddedStudents

def createSystemUser(first_name, last_name, album_number):
    password = album_number
    username = first_name + last_name
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create(username=username,
                                   email='jlennon@beatles.com',
                                   password=password,
                                   first_name=first_name,
                                   last_name=last_name)
        user.save()
        return user

    return None


def createMyUser(user):
    try:
        myUser = MyUser.objects.get(username=user.username)
    except MyUser.DoesNotExist:
        myUser = MyUser()
        myUser.username = user.username
        myUser.first_name = user.first_name
        myUser.last_name = user.last_name
        myUser.set_password(user.password)
        myUser.user = user
        myUser.save()
        return myUser
    return None


def createNewUserProfile(user):
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = UserProfile()
        profile.user = user
        profile.username = user.username
        profile.first_name = user.first_name
        profile.last_name = user.last_name
        profile.save()
        return profile
    return None


def createNewStudentUser(profile, album_number, group, request):
    try:
        student = StudentUser.objects.get(profile=profile)
    except StudentUser.DoesNotExist:
        student = StudentUser()
        student.profile = profile
        student.album_number = album_number
        student.group = group
        course_id = request.session.get('selected_course_id')
        course = get_object_or_404(Course, id=course_id)
        student.course = []
        student.save()
        student.courses.add(course)


def addStudentToSelectedCourse(album_number, request):
    student = get_object_or_404(StudentUser, album_number=album_number)
    course_id = request.session.get('selected_course_id')
    course = get_object_or_404(Course, id=course_id)
    if student.courses.filter(id=course_id).exists():
        return False
    else:
        student.courses.add(course)
        return True