from django.contrib.auth.models import User
from django.test import Client
from django.test import RequestFactory
from django.test import TestCase

from main.methods import createNewTutorUser
from main.models import MyUser
from main.views import createNewUserProfile
from tutor.methods import getTutorUserFromRequest


class TutorUserTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

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
        createNewTutorUser(profile)

    def test_get_tutor_user_from_request(self):
        client = Client()
        client.login(username='tutor', password='tutor')
        request = self.factory.get('/zpr/')
        request.user = self.user
        userFromRequest = getTutorUserFromRequest(request)
        self.assertEqual(userFromRequest.profile.user.user, self.user)