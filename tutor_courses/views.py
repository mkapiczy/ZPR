from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

from main.models import Course
from main.permissions import has_tutor_permissions
from tutor.methods import getTutorUserFromRequest
from tutor_courses.forms import CourseForm


class CoursesView(View):
    template_name = 'tutor_courses/courses_index.html'
    index_template = 'tutor/index.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if has_tutor_permissions(request.user):
            return super(CoursesView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('User has no access rights for viewing this page')

    def get(self, request):
        tutor = getTutorUserFromRequest(request)
        allCourses = Course.objects.all()
        templateCourses = populateTemplateCourses(allCourses, tutor)
        return render(request, self.template_name,
                      {'nbar': 'courses', 'courses': templateCourses})


class CourseCreate(View):
    form_class = CourseForm
    template_name = 'tutor_courses/course_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'nbar': 'courses', 'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            course = form.save(commit=False)

            try:
                course.save()
            except IntegrityError as e:
                return render(request, self.template_name,
                              {'nbar': 'projects', 'form': form, 'error_message': 'Taki kurs już istnieje!'})

            return redirect('tutor_courses:index')


def populateTemplateCourses(allCourses, tutor):
    templateCourses = []
    for course in allCourses:
        assigned = False
        for tutorInCourse in course.tutoruser_set.all():
            if tutorInCourse == tutor:
                assigned = True
        templateCourses.append(
            {'id': course.id, 'name': course.name, 'short_name': course.short_name,
             'tutoruser_set': course.tutoruser_set, 'assigned': assigned})

    return templateCourses
