from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from main.permissions import has_student_permissions
from main_posts.models import Post
from student.methods import get_student_user_from_request
from student_inbox.methods import refresh_inbox_status


class IndexView(View):
    template_name = 'student/index.html'
    login_url = 'main:login'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if has_student_permissions(request.user):
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

        student = get_student_user_from_request(request)
        student_courses = student.courses.all()
        request.session['courses'] = student_courses
        refresh_inbox_status(request, student)
        return render(request, self.template_name, {'posts': posts})

