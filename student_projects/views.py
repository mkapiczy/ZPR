from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from main.models import Project


from main.permissions import has_student_permissions, has_tutor_permissions


class ProjectsView(View):
    template_name = 'student_projects/projects_index.html'
    index_template = 'student/index.html'


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if has_student_permissions(request.user):
            return super(ProjectsView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('User has no access rights for viewing this page')

    def get(self, request):
        selected_course_id = request.session.get('selected_course_id')
        if (selected_course_id is not None):
            course_projects= Project.objects.filter(course=selected_course_id)
            return render(request, self.template_name,{'course_projects':course_projects})
        else:
            return redirect('student:index')