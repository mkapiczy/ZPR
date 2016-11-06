from django.db import models

from main.models import UserProfile


class TutorUser(models.Model):
    profile = models.ForeignKey(UserProfile)

    # totor fields

    class Meta:
        db_table = 'tutor_user'
