from django.conf.urls import url

from main.views import select_course
from . import views

app_name = 'student_inbox'

urlpatterns = [
    # /student/inbox/
    url(r'^$', views.InboxView.as_view(), name='index'),






]
