from django.conf.urls import url

from . import views

app_name = 'main'

urlpatterns = [
    # /zpr/
    url(r'^$', views.LoginView.as_view(), name='login'),

    url(r'register/$', views.UserFormView.as_view(), name='register'),

    url(r'login/$', views.LoginView.as_view(), name='login'),

    url(r'logout/$', views.LogoutView.as_view(), name='logout'),
]
