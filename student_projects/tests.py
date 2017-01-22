from django.contrib.auth.models import User
from django.test import RequestFactory
from django.test import TestCase

from main.methods import createNewTutorUser
from main.models import MyUser, Project, Course
from main.views import createNewUserProfile, createNewStudentUser
from student.models import ProjectTeam
from student_projects.methods import chosenStudentsAreValid, tutorAllowedTeamsNumberNotExceeded
from tutor.models import TutorCourse


class StudentProjectTestCase(TestCase):
    COURSE_ID = 1

    def setUp(self):
        self.factory = RequestFactory()

        self.user = User.objects.create_user(username='student', email='test@test', password='student')

        myUser = MyUser()
        myUser.username = self.user.username
        myUser.user = self.user
        myUser.password = self.user.password
        myUser.first_name = 'Student'
        myUser.last_name = 'Test'
        myUser.is_tutor = False
        myUser.save()

        profile = createNewUserProfile(myUser)

        tutor = createNewTutorUser(profile)

        project = Project()
        project.id = 1
        project.allowed_students_number = 3
        project.minimum_students_number = 2
        project.course_id = 1
        project.tutor_id = tutor.id
        project.save()

        self.tutor = tutor

    def test_chosenStudentsAreValid(self):
        projectWithMinimumStudents2AndMaximum3 = Project.objects.get(id=1)
        toManyChosenStudents = [1, 2, 3, 4, 5, 6];
        toLessChosenStudents = [1]
        okChosenStudents = [1, 2, 3]

        self.assertEqual(chosenStudentsAreValid(toManyChosenStudents, projectWithMinimumStudents2AndMaximum3), False)
        self.assertEqual(chosenStudentsAreValid(toLessChosenStudents, projectWithMinimumStudents2AndMaximum3), False)
        self.assertEqual(chosenStudentsAreValid(okChosenStudents, projectWithMinimumStudents2AndMaximum3), True)

    def test_tutorAllowedTeamsNumberNotExceeded(self):
        testCourse = Course(id=self.COURSE_ID)
        testCourse.save()

        tutorHas2AllowedTeamsNumber(self.tutor, testCourse)
        assign3TeamsToTutor(self.tutor, testCourse)

        tutorProject = Project.objects.get(id=1)

        self.assertEqual(tutorAllowedTeamsNumberNotExceeded(tutorProject), False)


def tutorHas2AllowedTeamsNumber(tutor, testCourse):
    tutorCourse = TutorCourse(tutor=tutor, courseId=testCourse.id, allowedTeamsNumber=2)
    tutorCourse.save()


def assign3TeamsToTutor(tutor, testCourse):
    testProject1 = Project(id=1, course=testCourse, tutor=tutor)
    testProject1.save()

    testProject2 = Project(id=2, course=testCourse, tutor=tutor)
    testProject2.save()

    testProject3 = Project(id=3, course=testCourse, tutor=tutor)
    testProject3.save()

    testTeam1 = ProjectTeam(id=1, project=testProject1, course=testCourse, accepted=True)
    testTeam1.save()
    testTeam2 = ProjectTeam(id=2, project=testProject2, course=testCourse, accepted=True)
    testTeam2.save()
    testTeam3 = ProjectTeam(id=3, project=testProject3, course=testCourse, accepted=True)
    testTeam3.save()

