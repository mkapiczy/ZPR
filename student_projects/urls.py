from django.conf.urls import url

from student_projects import views

app_name = 'student_projects'

urlpatterns = [
    url(r'^$', views.ProjectsView.as_view(), name='projects'),


]
