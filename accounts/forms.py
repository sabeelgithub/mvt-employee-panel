# forms.py
from django import forms

from .models import CustomUser


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=5, required=True)
    phone = forms.CharField(max_length=15, required=True) 
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password','phone']

    # Custom validation for unique username, email, and phone
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with this username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Custom validation to ensure phone is unique
        if CustomUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError("A user with this phone number already exists.")
        return phone

