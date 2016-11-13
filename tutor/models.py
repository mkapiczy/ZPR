from django.db import models

from main.models import UserProfile, Course


class TutorUser(models.Model):
    profile = models.ForeignKey(UserProfile)
    courses = models.ManyToManyField(Course)


    class Meta:
        db_table = 'tutor_user'

