from django.db import models

from main.models import UserProfile, Course


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


class TutorCourse(models.Model):
    tutor = models.ForeignKey(TutorUser)
    courseId = models.IntegerField()
    allowedTeamsNumber = models.IntegerField(default=10)
