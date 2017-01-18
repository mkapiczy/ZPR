from django.forms import forms


class SignedStudent:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class CreateProjectTeamForm(forms.Form):
    signed_students = []

