from django import forms

from .models import Employee

# class EmployeeForm(forms.ModelForm):
#     name = forms.CharField(max_length=150, required=True)
#     position = forms.CharField(max_length=150, required=True)
#     email = forms.CharField(max_length=150, required=True)

#     class Meta:
#         model = Employee
#         fields = ['name', 'position', 'email','custom_fields']
    
#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         # Get the instance of the employee (if it's being updated)
#         instance = self.instance

#         if instance and instance.email != email:  # Ensure the current employee's email is not checked
#             if Employee.objects.filter(email=email).exists():
#                 raise forms.ValidationError("This Email Is Already Taken By Someone Else")
        
#         return email
    

class EmployeeForm(forms.ModelForm):
    name = forms.CharField(max_length=150, required=True)
    position = forms.CharField(max_length=150, required=True)
    email = forms.CharField(max_length=150, required=True)
    field_order = forms.CharField(widget=forms.HiddenInput(), required=False)  # Hidden field to store order

    class Meta:
        model = Employee
        fields = ['name', 'position', 'email', 'custom_fields', 'field_order']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Get the instance of the employee (if it's being updated)
        instance = self.instance

        if instance and instance.email != email:  # Ensure the current employee's email is not checked
            if Employee.objects.filter(email=email).exists():
                raise forms.ValidationError("This Email Is Already Taken By Someone Else")
        
        return email
    
    def save(self, commit=True):
        # Save the form data
        instance = super().save(commit=False)
        
        # Capture the field order from the cleaned_data
        field_order = self.cleaned_data.get('field_order')
        if field_order:
            instance.field_order = field_order.split(',')  # Store field order as a list

        if commit:
            instance.save()
        
        return instance

