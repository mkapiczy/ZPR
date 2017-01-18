import csv
import os
from io import TextIOWrapper
from sqlite3 import IntegrityError

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DeleteView
from django.views.generic import UpdateView

from main.methods import delayErrorAlertFade, isFileCorrect, setWrongFileSessionParam
from main.models import Project
from main.permissions import has_tutor_permissions
from tutor.methods import getTutorUserFromRequest
from tutor_projects.forms import ProjectForm
from tutor_projects.methods import saveProject


class ProjectsView(View):
    template_name = 'tutor_projects/projects_index.html'
    index_template = 'tutor/index.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if has_tutor_permissions(request.user):
            return super(ProjectsView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('User has no access rights for viewing this page')

    def get(self, request):
        delayErrorAlertFade(request, 'wrongFile')
        selectedCourseId = request.session.get('selected_course_id')
        if (selectedCourseId is not None):
            tutor = getTutorUserFromRequest(request)
            tutorCourse = tutor.getTutorCourseByCourseId(selectedCourseId)

            allCourseProjects = Project.objects.filter(course=selectedCourseId)
            return render(request, self.template_name, {'nbar': 'projects', 'course_projects': allCourseProjects,
                                                        'tutorAllowedTeamsNumber': tutorCourse.allowedTeamsNumber})
        else:
            return redirect('tutor:index')


def read_projects_from_file(request):
    if isFileCorrect('projects_file', '.csv', request):
        file = TextIOWrapper(request.FILES['projects_file'].file, encoding='utf-8')
        reader = csv.reader(file, delimiter=',')
        descriptions = []
        for row in reader:
            if (row):
                project = Project()
                project.name = 'Projekt'
                project.description = row
                saveProject(project, request)

        request.session['desc'] = descriptions
        return redirect('tutor_projects:projects')
    else:
        setWrongFileSessionParam(request)
        return redirect('tutor_projects:projects')


class ProjectCreate(View):
    form_class = ProjectForm
    template_name = 'tutor_projects/project_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'nbar': 'projects', 'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            project = form.save(commit=False)

            try:
                saveProject(project, request)
            except IntegrityError as e:
                return render(request, self.template_name,
                              {'nbar': 'projects', 'form': form, 'error_message': 'Taki projekt już istnieje!'})

            return redirect('tutor_projects:projects')


class ProjectUpdate(UpdateView):
    template_name = 'tutor_projects/project_form.html'
    form_class = ProjectForm
    model = Project
    success_url = reverse_lazy('tutor_projects:projects')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProjectUpdate, self).dispatch(request, *args, **kwargs)


class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('tutor_projects:projects')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProjectDelete, self).dispatch(request, *args, **kwargs)


def plusTutorAllowedTeamsNumber(request):
    tutor = getTutorUserFromRequest(request)
    tutorCourse = tutor.getTutorCourseByCourseId(request.session.get('selected_course_id'))
    tutorCourse.allowedTeamsNumber += 1
    tutorCourse.save()
    return redirect('tutor_projects:projects')


def minusTutorAllowedTeamsNumber(request):
    tutor = getTutorUserFromRequest(request)
    tutorCourse = tutor.getTutorCourseByCourseId(request.session.get('selected_course_id'))
    if(tutorCourse.allowedTeamsNumber > 0):
        tutorCourse.allowedTeamsNumber -= 1
        tutorCourse.save()
    return redirect('tutor_projects:projects')


def vacate_project(request, pk):
    project = get_object_or_404(Project, id=pk)
    for projectTeam in project.projectteam_set.all():
        for student in projectTeam.studentuser_set.all():
            for studentProjectTeam in student.projectTeams.all():
                if studentProjectTeam == projectTeam:
                    student.removeProjectTeamForCourse(projectTeam.course.id)
                    student.save()
        projectTeam.project = None
        projectTeam.delete()

    project.setProjectAvailable()
    return redirect('tutor_projects:projects')
