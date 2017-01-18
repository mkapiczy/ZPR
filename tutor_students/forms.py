from django import forms


class StudentForm(forms.Form):

    album_number = forms.CharField(max_length=16, label="Nr albumu")
    status = forms.BooleanField(label="Status")
    group = forms.CharField(max_length=32,label="Grupa")
    first_name = forms.CharField(max_length=32,label="Imię")
    last_name = forms.CharField(max_length=32,label="Nazwisko")