from main.models import NewProjectTeamRequest, UserInbox, Message
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

def createNewProjectTeamMessage(project_team):
    title = 'Zaproszenie do grupa projektowa';
    text='Czy chcesz zaakceptować zaproszenie do grupy projektu: ' + project_team.project.name+ '\n';
    text += "Członkowie grupy: \n";
    for student in project_team.studentuser_set.all():
        text += student.profile.first_name + ' ' + student.profile.last_name + '\n'
    print(title)
    print(text)
    message = Message(title=title, text=text)
    message.save()
    return message
