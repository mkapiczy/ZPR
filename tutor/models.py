from django.db import models

from main.models import UserProfile, Course


class TutorUser(models.Model):
    profile = models.ForeignKey(UserProfile)
    courses = models.ManyToManyField(Course)
    #allowed_teams_number = models.IntegerField(default=10)

    class Meta:
        db_table = 'tutor_user'

