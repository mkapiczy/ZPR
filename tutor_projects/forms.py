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

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nazwa'
        self.fields['description'].label = 'Opis'
        self.fields['allowed_teams_number'].label = 'Liczba dozwolonych zespołów'
        self.fields['minimum_students_number'].label = 'Minimalna liczba studentów'
        self.fields['allowed_students_number'].label = 'Dozwolona liczba studentów'