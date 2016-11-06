from django.core.urlresolvers import reverse
from django.db import models

from main.models import UserProfile, Project

class ProjectTeam(models.Model):
    project = models.OneToOneField(Project)

class StudentUser(models.Model):
    profile = models.ForeignKey(UserProfile)

    # studentFields
    album_number = models.CharField(max_length=16)
    eres_id = models.CharField(max_length=16)
    status = models.BooleanField
    group = models.CharField(max_length=32)
    project_team = models.ForeignKey(ProjectTeam)

    class Meta:
        db_table = 'student_user'



class Album(models.Model):
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=250)
    genre = models.CharField(max_length=100)
    album_logo = models.FileField()

    def get_absolute_url(self):
        return reverse('student:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.album_title + ' - ' + self.artist


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10)
    song_title = models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title
