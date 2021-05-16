from django import forms
from .models import *

class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        exclude = ['user','institute']
        widgets = {
            'user_image':forms.FileInput
        }
class InstituteForm(forms.ModelForm):
    class Meta:
        model = Institute
        exclude = ['user','institute']
        widgets = {
            'user_image':forms.FileInput
        }

class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        exclude = ['user','institute']
        widgets = {
            'user_image':forms.FileInput
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['user','institute']
        widgets = {
            'user_image':forms.FileInput
        }

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        exclude = ['test_id','classroom','published']
