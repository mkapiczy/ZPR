from django.db import models

from main.models import UserProfile, Course, Project
from student.models import ProjectTeam


class TutorUser(models.Model):
    profile = models.ForeignKey(UserProfile)
    courses = models.ManyToManyField(Course)

    class Meta:
        db_table = 'tutor_user'

    def getTutorCourseByCourseId(self, selectedCourseId):
        for tutorCourse in self.tutorcourse_set.all():
            if tutorCourse.courseId == selectedCourseId:
                return tutorCourse
        tutorCourse = TutorCourse(tutor=self, courseId=selectedCourseId, allowedTeamsNumber=10)
        return tutorCourse

    def getTutorAllowedTeamsNumberByCourseId(self,courseId):
        return self.getTutorCourseByCourseId(courseId).allowedTeamsNumber

    def getAllTeamsAssignedToTutorForCourse(self, courseId):
        tutorTeams = []
        allTutorProjects = Project.objects.filter(tutor=self, course=courseId)
        for project in allTutorProjects:
            try:
                tutorTeams.append(ProjectTeam.objects.get(project=project, accepted=True))
            except ProjectTeam.DoesNotExist:
                pass
        return tutorTeams


class TutorCourse(models.Model):
    tutor = models.ForeignKey(TutorUser)
    courseId = models.IntegerField()
    allowedTeamsNumber = models.IntegerField(default=10)
