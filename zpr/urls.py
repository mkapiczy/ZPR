from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^zpr/', include('main.urls')),
    url(r'^zpr/student/', include('student.urls')),
    url(r'^zpr/tutor/', include('tutor.urls')),
    url(r'^zpr/tutor/posts/', include('tutor_posts.urls')),
    url(r'^zpr/tutor/projects/', include('tutor_projects.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
