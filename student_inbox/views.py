from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from main.models import NewProjectTeamMessage
from main.permissions import has_student_permissions
from student.methods import get_student_user_from_request
from student_inbox.methods import get_student_messages, refresh_inbox_status


class InboxView(View):
    template_name = 'student_inbox/inbox_index.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if has_student_permissions(request.user):
            return super(InboxView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('User has no access rights for viewing this page')

    def get(self, request):
        student = get_student_user_from_request(request)
        if student is not None:
            request.session['isStudentSignedToProject'] = student.project_team is not None
            inbox = get_student_messages(student)
            refresh_inbox_status(request, student)
            return render(request, self.template_name, {'inbox': inbox})
        else:
            return redirect('student_inbox:index')


def accept_project_team(request, pk):
    message = get_object_or_404(NewProjectTeamMessage, id=pk)
    message.accepted = True
    message.save()
    all_messages_accepted = True
    for msg in message.request.newprojectteammessage_set.all():
        if not msg.accepted:
            all_messages_accepted = False

    if all_messages_accepted:
        print('Request accepted!')
    return redirect('student_inbox:index')


def reject_project_team(request, pk):
    message = get_object_or_404(NewProjectTeamMessage, id=pk)
    message.user_inbox = None
    for student in message.request.project_team.studentuser_set.all():
        student.project_team = None
        student.save()
    message.request.project_team.project = None
    message.request.project_team.delete()
    message.request.delete()
    message.delete()
    print('Request deleted')
    return redirect('student_inbox:index')
