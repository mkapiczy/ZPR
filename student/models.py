from django.db import models
from django.core.urlresolvers import reverse
from main.models import UserProfile

class StudentUser(models.Model):
    profile = models.ForeignKey(UserProfile)

    # studentFields
    album_number = models.CharField(max_length=16)
    eres_id = models.CharField(max_length=16)
    status = models.BooleanField
    group = models.CharField(max_length=32)

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
