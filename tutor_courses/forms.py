from django import forms
from django.forms import Textarea

from main.models import Project, Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 15})
        }
        fields = ['name', 'short_name']

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nazwa'
        self.fields['short_name'].label = 'Nazwa skrócona'