from django.conf.urls import url

from tutor_students.views import CreateStudent, read_students_from_file
from . import views

app_name = 'tutor_students'

urlpatterns = [
    url(r'^$', views.StudentsView.as_view(), name='index'),


    url(r'^read_students_from_file/$', read_students_from_file, name='read_students_from_file'),
    #
    url(r'add/$', CreateStudent.as_view(), name='student-add'),
    url(r'(?P<pk>[0-9]+)/update$', views.UpdateStudent.as_view(), name='student-update'),
    url(r'(?P<pk>[0-9]+)/delete$', views.DeleteStudent.as_view(), name='student-delete'),

]
