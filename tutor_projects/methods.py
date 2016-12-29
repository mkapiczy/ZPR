from django.shortcuts import get_object_or_404

from main.models import Course, MyUser, UserProfile
from tutor.models import TutorUser


def saveProject(project, request):
    course_id = request.session.get('selected_course_id')
    course = get_object_or_404(Course, id=course_id)
    project.course = course

    myUser = get_object_or_404(MyUser, user=request.user)
    userProfile = get_object_or_404(UserProfile, user=myUser)
    userTutor = get_object_or_404(TutorUser, profile=userProfile)
    project.tutor = userTutor

    project.save()

