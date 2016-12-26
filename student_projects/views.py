from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from main.models import Project


from main.permissions import has_student_permissions, has_tutor_permissions
from student.views import get_student_user_from_request


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
            for project in course_projects:
                if(project.studentuser_set):
                    for student in project.studentuser_set.all():
                        print(student.album_number)
            student = get_student_user_from_request(request)
            student_signed_project = student.signed_project
            if student_signed_project is not None:
                request.session['signed_project_id'] = student_signed_project.id
            return render(request, self.template_name,{'course_projects':course_projects})
        else:
            return redirect('student:index')


def sing_to_project(request, pk):
    project_id = request.POST['project_id']
    project = get_object_or_404(Project, id=project_id)
    student = get_student_user_from_request(request)
    student.signed_project = project
    student.save()
    return redirect('student_projects:projects')