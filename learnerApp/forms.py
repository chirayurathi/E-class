from django import forms
from .models import *

class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        exclude = ['user','institute']
class InstituteForm(forms.ModelForm):
    class Meta:
        model = Institute
        exclude = ['user','institute']
class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        exclude = ['user','institute']
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['user','institute']