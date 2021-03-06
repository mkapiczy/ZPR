from django.db import models

from main.models import Project, Course, UserInbox


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
    projectTeams = models.ManyToManyField(ProjectTeam)
    signedProjects = models.ManyToManyField('main.Project')

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
        alreadySignedProject = self.getSignedProjectForCourse(courseId)
        if alreadySignedProject is not None:
            self.signedProjects.remove(alreadySignedProject)
        self.signedProjects.add(project)
        self.save()

    def removeSignedProjectForCourse(self, courseId):
        alreadySignedProject = self.getSignedProjectForCourse(courseId)
        if alreadySignedProject is not None:
            self.signedProjects.remove(alreadySignedProject)
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

    def removeProjectTeamForCourse(self, courseId):
        alreadyAssignedProjectTeam = self.getProjectTeamForCourse(courseId)
        if alreadyAssignedProjectTeam is not None:
            self.projectTeams.remove(alreadyAssignedProjectTeam)
            self.save()

    def isStudentSignedToCourseProjectTeam(self, courseId):
        alreadyAssignedProjectTeam = self.getProjectTeamForCourse(courseId)
        if alreadyAssignedProjectTeam is not None and alreadyAssignedProjectTeam.accepted:
            return True
        else:
            return False

    def getStudentInboxOrCreateIfNone(self):
        if self.profile.inbox is None:
            UserInbox.objects.get_or_create(user_profile=self.profile)
            inbox = UserInbox.objects.get(user_profile=self.profile)
            self.profile.inbox = inbox
            self.profile.save()
        return self.profile.inbox
