import csv
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

from main.models import Project, Course, MyUser, UserProfile
from main.permissions import has_tutor_permissions
from tutor.models import TutorUser
from tutor_projects.forms import ProjectForm


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
        selected_course_id = request.session.get('selected_course_id')
        if (selected_course_id is not None):
            course_projects= Project.objects.filter(course=selected_course_id)
            return render(request, self.template_name,{'course_projects':course_projects})
        else:
            return redirect('tutor:index')


def read_projects_from_file(request):
    file = request.FILES['projects_file']
    # print(request.FILES['projects_file'].read())
    #
    file = TextIOWrapper(request.FILES['projects_file'].file, encoding='utf-8')

    reader = csv.reader(file, delimiter=',')
    descriptions = []
    for row in reader:
        if(row):
            project = Project()
            project.name = 'Projekt'
            project.description = row
            saveProject(project, request)

    print(len(descriptions))
    request.session['desc'] = descriptions

    return redirect('tutor_projects:projects')


class ProjectCreate(View):
    form_class = ProjectForm
    template_name = 'tutor_projects/project_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            project = form.save(commit=False)

            try:
               saveProject(project, request)
            except IntegrityError as e:
                return render(request, self.template_name,
                              {'form': form, 'error_message': 'Taki projekt już istnieje!'})

            return redirect('tutor_projects:projects')

def saveProject(project, request):
    course_id = request.session.get('selected_course_id')
    course = get_object_or_404(Course, id=course_id)
    project.course = course

    myUser = get_object_or_404(MyUser, user=request.user)
    userProfile = get_object_or_404(UserProfile, user=myUser)
    userTutor = get_object_or_404(TutorUser, profile=userProfile)
    project.tutor = userTutor

    project.save()


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