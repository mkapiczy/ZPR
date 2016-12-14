from django.contrib.auth.models import User
from django import forms

from main.models import Project


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['name', 'description', 'allowed_teams_number', 'allowed_students_number']



