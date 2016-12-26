from django import forms
from django.forms import Textarea

from main.models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 15})
        }
        fields = ['name', 'description', 'allowed_teams_number', 'minimum_students_number', 'allowed_students_number']
