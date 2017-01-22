from django.conf.urls import url

from tutor_tutors import views
from tutor_tutors.views import CreateTutor

app_name = 'tutor_tutors'

urlpatterns = [
    url(r'^$', views.TutorsView.as_view(), name='index'),
    url(r'add/$', CreateTutor.as_view(), name='tutor-add'),
    url(r'(?P<pk>[0-9])/delete$', views.DeleteTutor.as_view(), name='tutor-delete'),

]
