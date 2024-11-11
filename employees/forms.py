from django import forms

from .models import Employee

class EmployeeForm(forms.ModelForm):
    name = forms.CharField(max_length=150, required=True)
    position = forms.CharField(max_length=150, required=True)
    email = forms.CharField(max_length=150, required=True)

    class Meta:
        model = Employee
        fields = ['name', 'position', 'email','custom_fields']  # Customize fields based on your model
