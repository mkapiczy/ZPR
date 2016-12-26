from django.conf.urls import url

from main.views import select_course
from . import views

app_name = 'student'

urlpatterns = [
    # /student/
    url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'^select_course/(?P<course_id>[0-9]+)/$', select_course, name='select-course'),

    # /student/{id}/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # /student/album/add
    url(r'album/add/$', views.AlbumCreate.as_view(), name='album-add'),
    # /student/album/{id}
    url(r'album/(?P<pk>[0-9]+)/$', views.AlbumUpdate.as_view(), name='album-update'),

    # /student/album/{id}/delete
    url(r'album/(?P<pk>[0-9]+)/delete/$', views.AlbumDelete.as_view(), name='album-delete'),


]
