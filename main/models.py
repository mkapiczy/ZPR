from django.contrib.auth.models import (AbstractBaseUser)
from django.contrib.auth.models import User
from django.db import models
from tutor.models import TutorUser
from student.models import StudentUser


class MyUser(User):
    # common fields
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_tutor = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.OneToOneField(MyUser)
    # common fields
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def is_student_user(self):
        if self.user.is_tutor:
            return False
        else:
            return True

    def is_tutor_user(self):
        if self.user.is_tutor:
            return True
        else:
            return False


class Course(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=16)
    tutors = models.ManyToManyField(TutorUser)
    students = models.ManyToManyField(StudentUser)


class Project(models.Model):
    name = models.CharField()
    description = models.CharField()
    allowed_teams_number = models.IntegerField(default=1)
    allowed_students_number = models.IntegerField()
    available = models.BooleanField(default=True)
    course = models.ForeignKey(Course)
