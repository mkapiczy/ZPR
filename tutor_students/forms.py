from django import forms


class StudentForm(forms.Form):

    album_number = forms.CharField(max_length=16)
    status = forms.BooleanField
    group = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    first_name = forms.CharField(max_length=32)
