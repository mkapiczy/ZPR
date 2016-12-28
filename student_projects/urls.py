from django.conf.urls import url

from student_projects import views
from student_projects.views import sing_to_project, CreateProjectTeamView, UserProjectTeamView

app_name = 'student_projects'

urlpatterns = [
    url(r'^$', views.ProjectsView.as_view(), name='projects'),
    url(r'(?P<pk>[0-9]+)/sign', sing_to_project, name='project-sign'),
    url(r'(?P<pk>[0-9]+)/create', CreateProjectTeamView.as_view(), name='project-create-team'),
    url(r'/userTeam', UserProjectTeamView.as_view(), name='project-team-view'),

]
