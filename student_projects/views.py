from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from main.models import Project, NewProjectTeamMessage
from main.permissions import has_student_permissions
from student.views import getStudentUserFromRequest
from student_inbox.methods import refreshInboxStatus
from student_projects.forms import CreateProjectTeamForm, SignedStudent
from student_projects.methods import getStudentInboxOrCreateIfNone, createNewProjectTeamRequest, \
    createProjectTeam, createNewProjectTeamMessage, getChosenStudentsFromRequest, chosenStudentsAreValid


class ProjectsView(View):
    template_name = 'student_projects/projects_index.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if has_student_permissions(request.user):
            return super(ProjectsView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('User has no access rights for viewing this page')

    def get(self, request):
        selectedCourseId = request.session.get('selected_course_id')
        if (selectedCourseId is not None):
            allCourseProjects = Project.objects.filter(course=selectedCourseId)

            student = getStudentUserFromRequest(request)
            studentSignedProject = student.getSignedProjectForCourse(selectedCourseId)
            studentProjectTeam = student.getProjectTeamForCourse(selectedCourseId)

            if studentSignedProject is not None:
                request.session['signed_project_id'] = studentSignedProject.id

            if (studentProjectTeam is not None):
                request.session['student_team_registered'] = True
            else:
                request.session['student_team_registered'] = False

            refreshInboxStatus(request, student)
            return render(request, self.template_name, {'course_projects': allCourseProjects})
        else:
            return redirect('student:index')


class UserProjectTeamView(View):
    template_name = 'student_projects/user_project_team_view.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if has_student_permissions(request.user):
            return super(UserProjectTeamView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('User has no access rights for viewing this page')

    def get(self, request):
        student = getStudentUserFromRequest(request)
        refreshInboxStatus(request, student)

        selectedCourseId = request.session.get('selected_course_id')
        if (selectedCourseId is not None):
            studentProjectTeam = student.getProjectTeamForCourse(selectedCourseId)
            if studentProjectTeam is not None:
                return render(request, self.template_name,
                              {'projectTeam': studentProjectTeam, 'project': studentProjectTeam.project})
            else:
                return render(request, self.template_name)
        else:
            return redirect('student:index')


def sing_to_project(request, pk):
    selectedCourseId = request.session.get('selected_course_id')

    project_id = request.POST['project_id']
    project = get_object_or_404(Project, id=project_id)
    student = getStudentUserFromRequest(request)
    studentSignedProjectForCourse = student.getSignedProjectForCourse(selectedCourseId)
    if studentSignedProjectForCourse is not None:
        student.signedProjects.remove(studentSignedProjectForCourse)
    student.signedProjects.add(project)
    student.save()

    return redirect('student_projects:projects')


class CreateProjectTeamView(View):
    form_class = CreateProjectTeamForm
    template_name = 'student_projects/create_team_form.html'

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
        selectedCourseId = request.session.get('selected_course_id')

        project = get_object_or_404(Project, id=pk)
        chosenStudents = getChosenStudentsFromRequest(request)

        if chosenStudentsAreValid(chosenStudents, project):
            projectTeam = createProjectTeam(project)

            projectTeamRequest = createNewProjectTeamRequest(projectTeam)

            for student in chosenStudents:
                student.setSignedProjectForCourse(project, selectedCourseId)
                student.setProjectTeamForCourse(projectTeam, selectedCourseId)
                student.save()

                newTeamMessage = NewProjectTeamMessage()
                newTeamMessage.request = projectTeamRequest
                newTeamMessage.message = createNewProjectTeamMessage(projectTeam)
                newTeamMessage.user_inbox = getStudentInboxOrCreateIfNone(student)
                newTeamMessage.save()

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
        signedStudents = project.studentuser_set.all()
        choices = []
        for student in signedStudents:
            choices.append(SignedStudent(student.id, student.profile.first_name + ' ' + student.profile.last_name))
        form = CreateProjectTeamForm()
        form.signed_students = choices
        return form
