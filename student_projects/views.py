from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from main.models import Project

from main.permissions import has_student_permissions, has_tutor_permissions
from student.models import StudentUser, ProjectTeam
from student.views import get_student_user_from_request
from student_projects.forms import CreateProjectTeamForm, SignedStudent


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
            course_projects = Project.objects.filter(course=selected_course_id)
            for project in course_projects:
                if (project.studentuser_set):
                    for student in project.studentuser_set.all():
                        print(student.album_number)
            student = get_student_user_from_request(request)
            student_signed_project = student.signed_project
            if student_signed_project is not None:
                request.session['signed_project_id'] = student_signed_project.id
            if(student.project_team is not None):
                request.session['student_team_registered'] = True
            return render(request, self.template_name, {'course_projects': course_projects})
        else:
            return redirect('student:index')


def sing_to_project(request, pk):
    project_id = request.POST['project_id']
    project = get_object_or_404(Project, id=project_id)
    student = get_student_user_from_request(request)
    student.signed_project = project
    student.save()
    return redirect('student_projects:projects')


class CreateProjectTeamView(View):
    form_class = CreateProjectTeamForm
    template_name = 'student_projects/create_team_form.html'
    index_template = 'student_projects/projects_index.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if has_student_permissions(request.user):
            return super(CreateProjectTeamView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('User has no access rights for viewing this page')

    def get(self, request, pk):
        form = self.populate_form(pk)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        project = get_object_or_404(Project, id=pk)
        chosen_students = self.get_chosen_students_from_request(request)

        if self.chosen_students_are_valid(chosen_students, project):
            project_team = create_project_team(project)
            set_project_unavailable(project)
            clear_project_signed_users_set(project)

            for student in chosen_students:
                student.project_team = project_team
                student.signed_project = project
                student.save()

            return redirect('student_projects:projects')
        else:
            form = self.populate_form(pk)
            errors = [
                'Wybierz liczbę studentów między: '
                + project.minimum_students_number.__str__() + ' - '
                + project.allowed_students_number.__str__() + ' !']
            return render(request, self.template_name, {'form': form, 'custom_errors': errors})

    def populate_form(self, pk):
        project = get_object_or_404(Project, id=pk)
        signed_students = project.studentuser_set.all()
        choices = []
        for student in signed_students:
            choices.append(SignedStudent(student.id, student.profile.first_name + ' ' + student.profile.last_name))
        form = CreateProjectTeamForm()
        form.signed_students = choices
        return form

    def chosen_students_are_valid(self, chosen_students, project):
        if (len(chosen_students) >= project.minimum_students_number
            and len(chosen_students) <= project.allowed_students_number):
            return True
        else:
            return False

    def get_chosen_students_from_request(self, request):
        students = request.POST.getlist('students')
        chosen_students = []
        for student_id in students:
            chosen_students.append(StudentUser.objects.get(id=student_id))
        return chosen_students

def create_project_team(project):
    project_team = ProjectTeam()
    project_team.project = project
    project_team.save()
    return project_team

def set_project_unavailable(project):
    project.available = False
    project.save()

def clear_project_signed_users_set(project):
    for student in project.studentuser_set.all():
        student.signed_project = None
        student.save()