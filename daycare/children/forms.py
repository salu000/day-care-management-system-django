from django import forms
from .models import Child, Guardian

class DateInput(forms.DateInput):
    input_type = 'date'

class GuardianForm(forms.ModelForm):
    class Meta:
        model = Guardian
        fields = ['name', 'phone', 'email', 'address', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'guardian_name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'id': 'guardian_phone', 'placeholder': '(555) 555-5555'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'guardian_email'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'id': 'guardian_address', 'placeholder': '1234 Main St'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['full_name', 'dob', 'gender', 'enrollment_class', 'start_date', 'photo', 'status']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'child_name'}),
            'dob': DateInput(attrs={'class': 'form-control', 'id': 'child_dob'}),
            'gender': forms.Select(attrs={'class': 'form-select', 'id': 'child_gender'}),
            'enrollment_class': forms.Select(attrs={'class': 'form-select', 'id': 'enroll_class'}),
            'start_date': DateInput(attrs={'class': 'form-control', 'id': 'start_date'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }