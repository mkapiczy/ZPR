from django.db import models
from datetime import datetime

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=10000)
    creation_time = models.DateTimeField(default=datetime.now, blank=True)
    general_post = models.BooleanField(default=False)
    course = models.ForeignKey('main.Course',on_delete=models.CASCADE)
    tutor = models.ForeignKey('tutor.TutorUser', on_delete=models.CASCADE)