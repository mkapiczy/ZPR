from django.conf.urls import url

from main.views import select_course
from . import views

app_name = 'tutor_posts'

urlpatterns = [
    # /tutor/posts/add
    url(r'add/$', views.PostCreate.as_view(), name='post-add'),
    # /tutor/posts/{id}/delete
    url(r'(?P<pk>[0-9]+)/delete/$', views.PostDelete.as_view(), name='post-delete'),
]
