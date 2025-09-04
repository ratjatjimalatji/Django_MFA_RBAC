from urllib import request
from .forms import RegisterForm, PostForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

@login_required(login_url="/login")
def home(request):
    return render(request, "home.html", {})

def authView(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # after a successful login the user is logged in & redirected to the home page
            messages.success(request, 'Account created successfully!')
            return redirect('/home/')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, "registration/signup.html", {"form": form})

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('/home/')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'registration/sign_up.html', {"form": form})

@login_required(login_url="/login")
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # accesses the user that i signed in
            post.save()
            return redirect('/home')  # Replace 'post_list' with your desired redirect URL
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})