from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from main.permissions import has_student_permissions
from student.views import get_student_user_from_request


class InboxView(View):
    template_name = 'student_inbox/inbox_index.html'
    index_template = 'student/index.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if has_student_permissions(request.user):
            return super(InboxView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('User has no access rights for viewing this page')

    def get(self, request):
        student = get_student_user_from_request(request)
        if student is not None:
            inbox = get_student_messages(student)
            return render(request, self.template_name, {'inbox': inbox})
        else:
            return redirect('student_inbox:index')


def get_student_messages(student):
    messages = []
    if student.profile.inbox and student.profile.inbox.newprojectteammessage_set:
        for msg in student.profile.inbox.newprojectteammessage_set.all():
            messages.append(msg)
    return messages
