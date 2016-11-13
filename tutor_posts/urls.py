from django.conf.urls import url

from main.views import select_course
from . import views

app_name = 'tutor_posts'

urlpatterns = [
    # /tutor/posts/add
    url(r'add/$', views.PostCreate.as_view(),  name='post-add'),
]
