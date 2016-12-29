from django.conf.urls import url

from tutor_courses.views import assignTutorToCourse
from . import views

app_name = 'tutor_courses'

urlpatterns = [
    url(r'^$', views.CoursesView.as_view(), name='index'),
    url(r'add/$', views.CourseCreate.as_view(), name='course-add'),
    url(r'(?P<pk>[0-9]+)/assign$', assignTutorToCourse, name='course-assing'),
]
