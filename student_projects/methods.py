from main.models import NewProjectTeamRequest, UserInbox
from student.models import ProjectTeam


def create_project_team(project):
    project_team = ProjectTeam()
    project_team.project = project
    project_team.save()
    return project_team


def create_new_project_team_request(project_team):
    new_team_request = NewProjectTeamRequest()
    new_team_request.project_team = project_team
    new_team_request.save()
    return new_team_request

def get_student_inbox_or_create_if_none(student):
    if student.profile.inbox is None:
        inbox = UserInbox(user_profile=student.profile)
        inbox.save()
        student.profile.inbox = inbox
        student.save()
    return student.profile.inbox

def set_project_unavailable(project):
    project.available = False
    project.save()


def clear_project_signed_users_set(project):
    for student in project.studentuser_set.all():
        student.signed_project = None
        student.save()