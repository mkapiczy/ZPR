from django.conf.urls import url

from student_projects import views
from student_projects.views import sing_to_project

app_name = 'student_projects'

urlpatterns = [
    url(r'^$', views.ProjectsView.as_view(), name='projects'),
    url(r'(?P<pk>[0-9]+)/sign', sing_to_project, name='project-sign'),

]
