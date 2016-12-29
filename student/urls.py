from django.conf.urls import url

from main.methods import select_course
from . import views

app_name = 'student'

urlpatterns = [
    # /student/
    url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'^select_course/(?P<course_id>[0-9]+)/$', select_course, name='select-course'),

]
