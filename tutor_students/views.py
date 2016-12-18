import csv
from io import TextIOWrapper
from sqlite3 import IntegrityError

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from main.models import MyUser, UserProfile, Course
from main.permissions import has_tutor_permissions
from main.views import uniqueContraintValidationRedirect
from student.models import StudentUser
from tutor_students.forms import StudentForm


class StudentsView(View):
    template_name = 'tutor_students/students_index.html'
    index_template = 'tutor/index.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if has_tutor_permissions(request.user):
            return super(StudentsView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('User has no access rights for viewing this page')

    def get(self, request):
        selected_course_id = request.session.get('selected_course_id')
        if (selected_course_id is not None):
            course_students = StudentUser.objects.filter(courses__in=[selected_course_id])
            return render(request, self.template_name, {'course_students': course_students})
        else:
            return redirect('tutor:index')


def read_projects_from_file(request):
    file = request.FILES['projects_file']
    # print(request.FILES['projects_file'].read())
    #
    file = TextIOWrapper(request.FILES['students_file'].file, encoding='utf-8')

    reader = csv.reader(file, delimiter=',')
    descriptions = []
    for row in reader:
        if (row):
            descriptions.append(row)

    print(len(descriptions))
    request.session['desc'] = descriptions

    return redirect('tutor_students:index')


class CreateStudent(View):
    form_class = StudentForm
    template_name = 'tutor_students/student_form.html'

    def get(self, request):
        form = StudentForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form_student_user = self.form_class(request.POST)

        if form_student_user.is_valid():
            password = form_student_user.cleaned_data['album_number']
            username = form_student_user.cleaned_data['first_name'] + form_student_user.cleaned_data['last_name']
            print(password)
            user = User.objects.create(username=username,
                                       email='jlennon@beatles.com',
                                       password=password,
                                       first_name=form_student_user.cleaned_data['first_name'],
                                       last_name=form_student_user.cleaned_data['last_name'])

            try:
                user.save()
                myUser = MyUser()
                myUser.username = user.username
                myUser.first_name = user.first_name
                myUser.last_name = user.last_name
                myUser.set_password(user.password)
                myUser.user = user
                myUser.save()
                profile = createNewUserProfile(myUser)
                createNewStudentUser(profile, request)
            except IntegrityError as e:
                return uniqueContraintValidationRedirect(self, request, form_student_user)

        return redirect('tutor_students:index')


def createNewUserProfile(user):
    profile = UserProfile()
    profile.user = user
    profile.username = user.username
    profile.first_name = user.first_name
    profile.last_name = user.last_name
    profile.save()
    return profile


def createNewStudentUser(profile, request):
    student = StudentUser()
    student.profile = profile
    course_id = request.session.get('selected_course_id')
    course = get_object_or_404(Course, id=course_id)
    student.course = []
    student.save()
    student.courses.add(course)
