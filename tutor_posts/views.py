from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.views.generic import DeleteView

from main.models import UserProfile
from main.permissions import has_tutor_permissions
from main_posts.models import Post
from tutor.methods import get_tutor_user_from_request
from tutor.models import TutorUser
from tutor_posts.forms import CreatePostForm


class PostCreate(CreateView):
    form_class = CreatePostForm
    model = Post
    template_name = 'tutor_posts/post_form.html'
    success_url = reverse_lazy('tutor:index')


    def form_valid(self, form):
        tutor = get_tutor_user_from_request(self.request)
        form.instance.tutor = tutor
        return super(PostCreate, self).form_valid(form)


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if has_tutor_permissions(request.user):
            return super(PostCreate, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('User has no access rights for viewing this page')


class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('tutor:index')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if has_tutor_permissions(request.user):
            return super(PostDelete, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('User has no access rights for viewing this page')
