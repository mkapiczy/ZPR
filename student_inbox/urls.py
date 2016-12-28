from django.conf.urls import url

from student_inbox.views import accept_project_team, reject_project_team
from . import views

app_name = 'student_inbox'

urlpatterns = [
    # /student/
    url(r'^$', views.InboxView.as_view(), name='index'),
    url(r'(?P<pk>[0-9]+)/accept', accept_project_team, name='team-accept'),
    url(r'(?P<pk>[0-9]+)/reject', reject_project_team, name='team-reject'),

]
