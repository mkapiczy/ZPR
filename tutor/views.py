from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from main.models import UserProfile
from main_posts.models import Post
from main.permissions import has_tutor_permissions
from .models import TutorUser


class IndexView(View):
    template_name = 'tutor/index.html'
    login_url = 'main:login'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if has_tutor_permissions(request.user):
            return super(IndexView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('User has no access rights for viewing this page')

    def get(self, request):
        posts = []
        if 'selected_course_id' in request.session:
            selected_course_id = request.session.get('selected_course_id')
            try:
                posts = Post.objects.filter(course=selected_course_id)
            except Post.DoesNotExist:
                pass
        else:
            posts = Post.objects.all()

        user_profile = UserProfile.objects.get(user=request.user)
        tutor = TutorUser.objects.get(profile_id=user_profile.id)
        tutor_courses = tutor.courses.all()
        request.session['courses'] = tutor_courses
        return render(request, self.template_name, {'posts': posts})

