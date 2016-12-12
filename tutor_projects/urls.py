from django.conf.urls import url

from main.views import select_course
from tutor_projects.views import read_projects_from_file

from . import views

app_name = 'tutor_projects'

urlpatterns = [
    url(r'^$', views.ProjectsView.as_view(), name='projects'),


    url(r'^read_projects_from_file/$', read_projects_from_file, name='read_projects_from_file'),

]
