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
    projectTeams = models.ManyToManyField(ProjectTeam, null=True)
    signedProjects = models.ManyToManyField('main.Project', null=True)

    class Meta:
        db_table = 'student_user'

    def getCourseById(self, courseId):
        for course in self.courses.all():
            if course.id == courseId:
                return course
        return None

    def getSignedProjectForCourse(self, courseId):
        for project in self.signedProjects.all():
            if project.course.id == courseId:
                return project
        return None

    def setSignedProjectForCourse(self, project, courseId):
        alreadySignedCourse = self.getSignedProjectForCourse(courseId)
        if alreadySignedCourse is not None:
            self.signedProjects.remove(alreadySignedCourse)
        self.signedProjects.add(project)
        self.save()

    def getProjectTeamForCourse(self, courseId):
        for team in self.projectTeams.all():
            if team.course.id == courseId:
                return team
        return None

    def setProjectTeamForCourse(self, projectTeam, courseId):
        alreadyAssignedProjectTeam = self.getProjectTeamForCourse(courseId)
        if alreadyAssignedProjectTeam is not None:
            self.projectTeams.remove(alreadyAssignedProjectTeam)
        self.projectTeams.add(projectTeam)
        self.save()
