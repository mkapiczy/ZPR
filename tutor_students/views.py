import csv
import re
from io import TextIOWrapper
from sqlite3 import IntegrityError

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from main.methods import delayErrorAlertFade, setWrongFileSessionParam, isFileCorrect
from main.models import MyUser, UserProfile, Course
from main.permissions import has_tutor_permissions
from main.views import uniqueContraintValidationRedirect
from student.models import StudentUser
from tutor_students.forms import StudentForm
from tutor_students.methods import addStudentToSelectedCourse, createNewStudentUser, createNewUserProfile, createMyUser, \
    createSystemUser, setNotAddedStudentsRequestParam


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
        delayErrorAlertFade(request,'notAddedStudents')
        selected_course_id = request.session.get('selected_course_id')
        if (selected_course_id is not None):
            course_students = StudentUser.objects.filter(courses__in=[selected_course_id])
            return render(request, self.template_name, {'nbar': 'students', 'course_students': course_students})
        else:
            return redirect('tutor:index')


class CreateStudent(View):
    form_class = StudentForm
    template_name = 'tutor_students/student_form.html'

    def get(self, request):
        form = StudentForm()
        return render(request, self.template_name, {'nbar': 'students', 'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            album_number = form.cleaned_data['album_number']
            group = form.cleaned_data['group']
            notAddedStudents = []
            try:
                user = createSystemUser(first_name, last_name, album_number)
                if (user is not None):
                    myUser = createMyUser(user)
                    profile = createNewUserProfile(myUser)
                    createNewStudentUser(profile, album_number, group, request)
                else:
                    if (not addStudentToSelectedCourse(album_number, request)):
                        notAddedStudents.append(first_name + ' ' + last_name)
            except IntegrityError as e:
                return uniqueContraintValidationRedirect(self, request, form)

        setNotAddedStudentsRequestParam(notAddedStudents, request)
        return redirect('tutor_students:index')


class UpdateStudent(View):
    form_class = StudentForm
    template_name = 'tutor_students/student_form.html'

    def get(self, request, pk):
        student_id = request.GET['student_id']
        if (student_id is not None):
            student = get_object_or_404(StudentUser, id=student_id)
            form = StudentForm(
                {'album_number': student.album_number, 'group': student.group, 'first_name': student.profile.first_name,
                 'last_name': student.profile.last_name})
            form.fields['first_name'].widget.attrs['readonly'] = True
            form.fields['last_name'].widget.attrs['readonly'] = True
            return render(request, self.template_name, {'nbar': 'students', 'form': form})
        else:
            return redirect('tutor_students:index')

    def post(self, request, pk):
        form = self.form_class(request.POST)

        if form.is_valid():
            student_id = pk
            if (student_id is not None):
                student = get_object_or_404(StudentUser, id=student_id)
                album_number = form.cleaned_data['album_number']
                group = form.cleaned_data['group']
                student.album_number = album_number
                student.group = group
                try:
                    student.save()
                except IntegrityError as e:
                    return uniqueContraintValidationRedirect(self, request, form)

        return redirect('tutor_students:index')


class DeleteStudent(View):
    def post(self, request, pk):
        student_id = request.POST['student_id']

        if student_id is not None:
            student = get_object_or_404(StudentUser, id=student_id)
            profile = get_object_or_404(UserProfile, id=student.profile.id)
            myUser = get_object_or_404(MyUser, id=profile.user.id)
            user = get_object_or_404(User, id=myUser.user.id)

            try:
                student.delete()
                profile.delete()
                myUser.delete()
                user.delete()
            except User.DoesNotExist:
                messages.error(request, "User does not exist")
                return render(request, 'tutor_students/students_index.html', {'nbar': 'students'})

            except Exception as e:
                return render(request, 'tutor_students/students_index.html', {'nbar': 'students', 'errors': e})

        return redirect('tutor_students:index')


def read_students_from_file(request):
    if isFileCorrect('students_file', '.csv', request):
        file = TextIOWrapper(request.FILES['students_file'].file, encoding='utf-8')
        reader = csv.reader(file, delimiter=';')
        notAddedStudents = []
        for row in reader:
            if (row):
                if (len(row) > 1 and not re.match("Nr", row[0])):
                    first_name = row[2].split(' ', 1)[0]
                    last_name = row[1]
                    album_number = row[3]
                    group = row[6]

                    try:
                        user = createSystemUser(first_name, last_name, album_number)
                        if user is not None:
                            myUser = createMyUser(user)
                            profile = createNewUserProfile(myUser)
                            createNewStudentUser(profile, album_number, group, request)
                        else:
                            if (not addStudentToSelectedCourse(album_number, request)):
                                notAddedStudents.append(first_name + ' ' + last_name)
                    except IntegrityError as e:
                        notAddedStudents.append([first_name + ' ' + last_name])
                        pass
        setNotAddedStudentsRequestParam(notAddedStudents, request)
        return redirect('tutor_students:index')
    else:
        setWrongFileSessionParam(request)
        return redirect('tutor_projects:projects')

def delete_all_students(request):
    selectedCourseId = request.session.get('selected_course_id')
    course = Course.objects.get(id=selectedCourseId)
    for student in course.studentuser_set.all():
        student.courses.remove(course)
        student.save()
    return redirect('tutor_students:index')