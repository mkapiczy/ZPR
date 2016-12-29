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


def deleteNotAcceptedProjectTeamsAndTheirRequests(projectTeam):
    allProjectTeamsAssignedToThisProject = ProjectTeam.objects.filter(project=projectTeam.project)
    for projectTeam in allProjectTeamsAssignedToThisProject:
        if not projectTeam.accepted:
            projectTeam.project = None
            projectTeam.course = None
            for student in projectTeam.studentuser_set.all():
                student.removeSignedProjectForCourse(projectTeam.course.id)
                student.removeProjectTeamForCourse(projectTeam.course.id)
            for request in projectTeam.newprojectteamrequest_set.all():
                deleteTeamRequestAssignedToMessage(request)
            projectTeam.delete()