from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

verificador_matricula = RegexValidator(r"(^[0-9]{2}\/)([0-9]+)", "Sua matricula deve possuir xx/xxxxxx")

class SignUpForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    matricula = forms.CharField(label = "Enter Matricula", required=True, validators=[verificador_matricula])
    fullname = forms.CharField(label = "Enter Full name", required=True)
    email = forms.EmailField(label='Enter email', required=True)
    password1 = forms.CharField(label='Enter password', required=True , widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', required=True , widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        user.matricula = self.cleaned_data['matricula'],
        user.fullname =  self.cleaned_data['fullname'],
        user.save()

        return user

class LoginForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    password1 = forms.CharField(label='Enter password', required=True , widget=forms.PasswordInput)
