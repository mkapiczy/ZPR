from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.test import Client
from django.test import RequestFactory
from django.test import TestCase

from main.models import MyUser
from main.views import createNewUserProfile, createNewTutorUser, createNewStudentUser


class MainTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        self.tutorUser = User.objects.create_user(username='tutor', email='test@test', password='tutor')

        tutorUser = MyUser()
        tutorUser.username = self.tutorUser.username
        tutorUser.user = self.tutorUser
        tutorUser.password = self.tutorUser.password
        tutorUser.is_tutor = True
        tutorUser.save()
        profile = createNewUserProfile(tutorUser)
        createNewTutorUser(profile)

        self.studentUser = User.objects.create_user(username='student', email='test@test', password='student')

        studentUser = MyUser()
        studentUser.username = self.studentUser.username
        studentUser.user = self.studentUser
        studentUser.password = self.studentUser.password
        studentUser.is_tutor = False
        studentUser.save()

        profile = createNewUserProfile(studentUser)
        createNewStudentUser(profile)

    def test_main_page(self):
        client = Client()
        response = client.get('/zpr/')
        self.assertEqual(response.status_code, 200)

    def test_authenticate_tutor(self):
        client = Client()
        client.login(username='tutor', password='tutor')
        response = client.get('/zpr/')
        self.assertRedirects(response, '/zpr/tutor/', status_code=302, target_status_code=200, host=None,
                             msg_prefix='', fetch_redirect_response=True)

    def test_authenticate_student(self):
        client = Client()
        client.login(username='student', password='student')
        response = client.get('/zpr/')
        self.assertRedirects(response, '/zpr/student/', status_code=302, target_status_code=200, host=None,
                             msg_prefix='', fetch_redirect_response=True)
