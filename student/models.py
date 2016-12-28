from django.db import models

from main.models import Project, Course


class ProjectTeam(models.Model):
    project = models.ForeignKey(Project)
    accepted = models.BooleanField(default=False)
    course = models.ForeignKey('main.Course', null=True)

class StudentUser(models.Model):
    profile = models.ForeignKey('main.UserProfile')
    album_number = models.CharField(max_length=16)
    eres_id = models.CharField(max_length=16)
    status = models.BooleanField
    group = models.CharField(max_length=32)
    courses = models.ManyToManyField(Course)
    project_teams = models.ManyToManyField(ProjectTeam, null=True)
    signed_projects = models.ManyToManyField('main.Project', null=True)

    class Meta:
        db_table = 'student_user'