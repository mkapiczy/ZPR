from datetime import datetime

from django.contrib.auth.models import (AbstractBaseUser)
from django.contrib.auth.models import User
from django.db import models


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
    tutors = models.ManyToManyField('tutor.TutorUser')
    students = models.ManyToManyField('student.StudentUser')


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=5000)
    allowed_teams_number = models.IntegerField(default=1)
    allowed_students_number = models.IntegerField()
    available = models.BooleanField(default=True)
    course = models.ForeignKey(Course)
    signed_students = models.ForeignKey('student.StudentUser')
    # project_team = models.OneToOneField('student.ProjectTeam')
    # OneToMany
    tutor = models.ForeignKey('tutor.TutorUser')


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=10000)
    creation_time = models.DateTimeField(default=datetime.now, blank=True)
    general_post = models.BooleanField(default=False)
    course = models.OneToOneField('main.Course')
    tutor = models.OneToOneField('tutor.TutorUser')
