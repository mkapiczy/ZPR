from django.contrib import admin
from .models import Album
from .models import Song
from .models import ProjectTeam, StudentUser

admin.site.register(Album)
admin.site.register(Song)
admin.site.register(ProjectTeam)
admin.site.register(StudentUser)