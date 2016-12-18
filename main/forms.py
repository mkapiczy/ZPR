from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import MyUser


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name','is_tutor', 'password']





