from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from main.permissions import has_student_permissions
from main_posts.models import Post
from student.methods import getStudentUserFromRequest
from student_inbox.methods import refreshInboxStatus


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
        selectedCourseId = request.session.get('selected_course_id')
        if selectedCourseId is not None:
            try:
                posts = Post.objects.filter(course=selectedCourseId).order_by('-creation_time')
            except Post.DoesNotExist:
                pass
        else:
            posts = Post.objects.all().order_by('-creation_time')

        student = getStudentUserFromRequest(request)
        studentCourses = student.courses.all()
        request.session['courses'] = studentCourses
        refreshInboxStatus(request, student)
        return render(request, self.template_name, {'nbar': 'home', 'posts': posts})
