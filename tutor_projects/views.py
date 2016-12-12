import csv
from io import TextIOWrapper

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect


# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

from main.permissions import has_tutor_permissions


class ProjectsView(View):
    template_name = 'tutor_projects/projects_form.html'
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
            return render(request, self.template_name)
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
           descriptions.append(row)
    print(len(descriptions))
    request.session['desc'] = descriptions

    return redirect('tutor_projects:projects')