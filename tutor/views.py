from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from main.permissions import has_tutor_permissions
from main_posts.models import Post
from tutor.methods import get_tutor_user_from_request


class IndexView(View):
    template_name = 'tutor/index.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if has_tutor_permissions(request.user):
            return super(IndexView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('User has no access rights for viewing this page')

    def get(self, request):
        posts = []
        selectedCourseId = request.session.get('selected_course_id')
        if selectedCourseId is not None:
            try:
                posts = Post.objects.filter(course=selectedCourseId)
            except Post.DoesNotExist:
                pass
        else:
            posts = Post.objects.all()

        tutor = get_tutor_user_from_request(request)
        tutorCourses = tutor.courses.all()
        request.session['courses'] = tutorCourses
        return render(request, self.template_name, {'posts': posts})
