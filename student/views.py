from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Album


class IndexView(generic.ListView):
    template_name = 'student/index.html'
    context_object_name = 'all_albums'
    login_url = 'main:login'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Album.objects.all()


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
    success_url = reverse_lazy('music:index')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AlbumDelete, self).dispatch(request, *args, **kwargs)

