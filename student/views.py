from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseForbidden
from main.models import UserProfile
from .models import Album, StudentUser
from main.permissions import has_student_permissions


class IndexView(View):
    template_name = 'student/index.html'
    context_object_name = 'all_albums'
    login_url = 'main:login'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if has_student_permissions(request.user):
            return super(IndexView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('User has no access rights for viewing this page')

    def get(self, request):
        all_albums = Album.objects.all()
        user_profile = UserProfile.objects.get(user=request.user)
        student = StudentUser.objects.get(profile_id=user_profile.id)
        student_courses = student.courses.all()
        return render(request, self.template_name, {'all_albums': all_albums, 'courses': student_courses})


class DetailView(generic.DetailView):
    model = Album
    template_name = 'student/detail.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DetailView, self).dispatch(request, *args, **kwargs)


class AlbumCreate(CreateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AlbumCreate, self).dispatch(request, *args, **kwargs)


class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AlbumUpdate, self).dispatch(request, *args, **kwargs)


class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('student:index')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AlbumDelete, self).dispatch(request, *args, **kwargs)

