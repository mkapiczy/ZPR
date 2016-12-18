from django.conf.urls import url

from main.views import select_course
from tutor_projects.views import read_projects_from_file

from . import views

app_name = 'tutor_projects'

urlpatterns = [
    url(r'^$', views.ProjectsView.as_view(), name='projects'),


    url(r'^read_projects_from_file/$', read_projects_from_file, name='read_projects_from_file'),

    url(r'add/$', views.ProjectCreate.as_view(), name='project-add'),
    url(r'(?P<pk>[0-9]+)/update$', views.ProjectUpdate.as_view(), name='project-update'),
    url(r'(?P<pk>[0-9]+)/delete$', views.ProjectDelete.as_view(), name='project-delete'),

]
