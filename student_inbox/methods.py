from django.shortcuts import get_object_or_404

from main.models import NewProjectTeamMessage
from student.models import ProjectTeam


def get_student_messages(student):
    messages = []
    if student.profile.inbox and student.profile.inbox.newprojectteammessage_set:
        for msg in student.profile.inbox.newprojectteammessage_set.all():
            messages.append(msg)
    return messages

def refresh_inbox_status(request, student):
    inbox = get_student_messages(student)
    unread_messages_amount = 0
    for message in inbox:
        if not message.read:
            unread_messages_amount += 1
    request.session['inbox'] = inbox
    request.session['unread_messages_size'] = unread_messages_amount

def markAllMessagesAsRead(inbox):
    for message in inbox:
        message.read = True
        message.save()


def allMessagesAssignedToThisTeamRequestAreAccepted(message):
    all_messages_accepted = True
    for msg in message.request.newprojectteammessage_set.all():
        if not msg.accepted:
            all_messages_accepted = False
    return all_messages_accepted


def acceptSingleTeamMessage(message_id):
    message = get_object_or_404(NewProjectTeamMessage, id=message_id)
    message.accepted = True
    message.save()
    return message


def acceptProjectTeamAssignedToMessage(message):
    project_team = message.request.project_team
    project_team.accepted = True
    project_team.save()
    project_team.project.available = False
    project_team.project.save()
    return project_team


def deleteTeamRequestAssignedToMessage(teamRequest):
    for msg in teamRequest.newprojectteammessage_set.all():
        msg.user_inbox = None
        msg.delete()
    teamRequest.project_team = None
    teamRequest.delete()


def deleteNotAcceptedProjectTeamsAndTheirRequests(project_team):
    all_project_teams_assigned_to_this_project = ProjectTeam.objects.filter(project=project_team.project)
    for project_team in all_project_teams_assigned_to_this_project:
        if not project_team.accepted:
            project_team.project = None
            for student in project_team.studentuser_set:
                student.signed_project = None
                student.project_team = None
                student.save()
            for request in project_team.newprojectteamrequest_set.all():
                deleteTeamRequestAssignedToMessage(request)
            project_team.delete()