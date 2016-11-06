from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic

from student.models import Album


class IndexView(generic.ListView):
    template_name = 'tutor/index.html'
    context_object_name = 'all_albums'
    login_url = 'main:login'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Album.objects.all()
