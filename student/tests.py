from django.contrib.auth.models import User
from django.test import Client
from django.test import RequestFactory
from django.test import TestCase

from main.models import MyUser
from main.views import createNewUserProfile, createNewStudentUser
from student.methods import getStudentUserFromRequest


class StudentUserTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        self.user = User.objects.create_user(username='student', email='test@test', password='student')

        studentUser = MyUser()
        studentUser.username = self.user.username
        studentUser.user = self.user
        studentUser.password = self.user.password
        studentUser.first_name = 'Student'
        studentUser.last_name = 'Test'
        studentUser.is_tutor = False
        studentUser.save()

        profile = createNewUserProfile(studentUser)
        createNewStudentUser(profile)

    def test_get_student_user_from_request(self):
        client = Client()
        client.login(username='student', password='student')
        request = self.factory.get('/zpr/')
        request.user = self.user
        userFromRequest = getStudentUserFromRequest(request)
        self.assertEqual(userFromRequest.profile.user.user, self.user)
