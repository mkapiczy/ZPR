from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from student.models import Album
from main.models import UserProfile
from .models import TutorUser


class IndexView(View):
    template_name = 'tutor/index.html'
    context_object_name = 'all_albums'
    login_url = 'main:login'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        all_albums = Album.objects.all()
        user = request.user
        user_profile = UserProfile.objects.get(user=request.user)
        tutor = TutorUser.objects.get(profile_id=user_profile.id)
        tutor_courses = tutor.courses.all()
        return render(request, self.template_name, {'all_albums': all_albums, 'courses': tutor_courses})
