from django import forms


class TutorForm(forms.Form):

    first_name = forms.CharField(max_length=32,label="Imię")
    last_name = forms.CharField(max_length=32,label="Nazwisko")
    password = forms.CharField(widget=forms.PasswordInput)
