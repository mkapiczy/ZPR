from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase

from main.methods import createNewTutorUser
from main.models import MyUser
from main.views import createNewUserProfile
from tutor.methods import getTutorUserFromRequest
from tutor.models import TutorCourse


class TutorAllowedTeamsNumberTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tutor', email='test@test', password='tutor')

        myUser = MyUser()
        myUser.username = self.user.username
        myUser.user = self.user
        myUser.password = self.user.password
        myUser.first_name = 'Tutor'
        myUser.last_name = 'Test'
        myUser.is_tutor = True
        myUser.save()

        profile = createNewUserProfile(myUser)

        tutor = createNewTutorUser(profile)

        tutorCourse = TutorCourse(tutor=tutor, courseId=1, allowedTeamsNumber=2)
        tutorCourse.save()

        self.client = Client()
        self.client.login(username='tutor', password='tutor')


    def test_minusTutorAllowedTeamsNumber(self):
        session = self.client.session
        session['selected_course_id'] = 1
        session.save()
        request = self.client.post('/zpr/tutor/projects/teamsNumber/minus')
        request.user = self.user
        userFromRequest = getTutorUserFromRequest(request)
        self.assertEqual(userFromRequest.getTutorAllowedTeamsNumberByCourseId(1), 1)

    def test_plusTutorAllowedTeamsNumber(self):
        session = self.client.session
        session['selected_course_id'] = 1
        session.save()
        request = self.client.post('/zpr/tutor/projects/teamsNumber/plus')
        request.user = self.user
        userFromRequest = getTutorUserFromRequest(request)
        self.assertEqual(userFromRequest.getTutorAllowedTeamsNumberByCourseId(1), 3)
