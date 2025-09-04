from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    firstname = forms.CharField(required=True, max_length=30)
    lastname = forms.CharField(required=True, max_length=30)
    role = forms.ChoiceField(choices=[('user', 'User'), ('manager', 'Manager'), ('admin', 'Admin'), ('guest', 'Guest')], required=True)

    class Meta:
        model = User
        fields = ["username", "firstname", "lastname", "role", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["firstname"]
        user.last_name = self.cleaned_data["lastname"]
        
        if commit:
            user.save()
            # You might want to save the role to a user profile model
            # For now, we'll skip role saving since it's not part of the default User model
        return user

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'text_content', 'document', 'image']