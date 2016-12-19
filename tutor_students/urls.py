from django.conf.urls import url

from tutor_students.views import CreateStudent
from . import views

app_name = 'tutor_students'

urlpatterns = [
    url(r'^$', views.StudentsView.as_view(), name='index'),


    # url(r'^read_projects_from_file/$', read_projects_from_file, name='read_projects_from_file'),
    #
    url(r'add/$', CreateStudent.as_view(), name='student-add'),
    # url(r'(?P<pk>[0-9]+)/update$', views.ProjectUpdate.as_view(), name='project-update'),
    url(r'(?P<pk>[0-9]+)/delete$', views.DeleteStudent.as_view(), name='student-delete'),

]
