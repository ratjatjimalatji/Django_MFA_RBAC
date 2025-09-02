from urllib import request
from .forms import RegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout, authenticate 


@login_required
def home(request):
 return render(request, "home.html", {})


def authView(request):
 if request.method == "POST":
  form = RegisterForm(request.POST or None)
  if form.is_valid():
   user = form.save()
   login(request, user) # after a successful login the user is logged in & redirected to the home page
   return redirect('/home')
   return redirect("base:login")
 else:
  form = RegisterForm()
 return render(request, "registration/signup.html", {"form": form})

def sign_up(request):
  if request.method =='POST':
    form = RegisterForm(request.POST)
  else:
    form = RegisterForm()

  return render(request, 'registration/sign_up.html', {"form": form})