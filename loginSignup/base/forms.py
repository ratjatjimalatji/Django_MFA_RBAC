from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Image, Document

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    firstname = forms.CharField(required=True, max_length=30)
    lastname = forms.CharField(required=True, max_length=30)
   
    class Meta:
        model = User
        fields = ["username", "firstname", "lastname", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["firstname"]
        user.last_name = self.cleaned_data["lastname"]
        
        if commit:
            user.save()
        return user

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description']
        
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'image', 'description']
        
        
    # def __init__(self, *args, **kwargs):
    #     self.user = kwargs.pop('user', None)
    #     super().__init__(*args, **kwargs)

    def save(self, commit=True):
        image = super().save(commit=False)
        if self.user:
            image.author = self.user
        if commit:
            image.save()
        return image

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'document', 'description']
    # def __init__(self, *args, **kwargs):
    #     self.user = kwargs.pop('user', None)
    #     super().__init__(*args, **kwargs)

    def save(self, commit=True):
        document = super().save(commit=False)
        if self.user:
            document.author = self.user
        if commit:
            document.save()
        return document
    

class ConfidentialForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'document', 'description']
