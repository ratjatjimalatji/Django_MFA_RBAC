from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# allows us to customize the registration form for the user
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    firstname = forms.CharField(required=True)
    lastname = forms.CharField(required=True)
    role = forms.ChoiceField(choices=[('user', 'User'), ('manager', 'Manager'), ('admin', 'Admin'), ('guest', 'Guest')], required=True)

    class Meta:
        model = User
        fields = ["firstname", "lastname", "role", "email", "password1", "password2"]
