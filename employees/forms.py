from django import forms

from .models import Employee

class EmployeeForm(forms.ModelForm):
    name = forms.CharField(max_length=150, required=True)
    position = forms.CharField(max_length=150, required=True)
    email = forms.CharField(max_length=150, required=True)

    class Meta:
        model = Employee
        fields = ['name', 'position', 'email','custom_fields']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Get the instance of the employee (if it's being updated)
        instance = self.instance

        if instance and instance.email != email:  # Ensure the current employee's email is not checked
            if Employee.objects.filter(email=email).exists():
                raise forms.ValidationError("This Email Is Already Taken By Someone Else")
        
        return email
