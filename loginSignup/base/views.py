from urllib import request
from .forms import RegisterForm, PostForm, ImageForm, DocumentForm, ConfidentialForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login
from django.contrib import messages
from .models import Post

@login_required(login_url="/login")
def home(request):
    posts = Post.objects.all()

    if request.method == "POST":
        post_id = request.POST.get("post-id")
        post = Post.objects.filter(id=post_id).first()
        if post and (post.author == request.user or request.user.has_perm("base.delete_post")):
            post.delete()
        print(post_id)

    return render(request, "home.html", {"posts": posts})

def authView(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            messages.success(request, 'Account created successfully!')
            return redirect('/home/') # after a successful login the user is logged in & redirected to the home page
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
@permission_required("base.add_post", login_url="/login", raise_exception=True)
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/home")
    else:
        form = PostForm()

    return render(request, 'create_post.html', {"form": form})


@login_required(login_url="/login")
#@permission_required("base.add_image", login_url="/login", raise_exception=True)
def create_image(request):
      if request.method == 'POST':
          form = ImageForm(request.POST, request.FILES)
          if form.is_valid():
            image = form.save(commit=False)
            image.author = request.user
            image.save()
            return redirect("/home")
          else:
            form = ImageForm()

          return render(request, 'create_image.html', {"form": form})
      else:
          form = ImageForm()

      return render(request, 'create_image.html', {"form": form})

@login_required(login_url="/login")
#@permission_required("base.add_document", login_url="/login", raise_exception=True)
def create_document(request):
      if request.method == 'POST':
          form = DocumentForm(request.POST, request.FILES)
          if form.is_valid():
            document = form.save(commit=False)
            document.author = request.user
            document.save()
            return redirect("/home")
          else:
            form = DocumentForm()

          return render(request, 'create_document.html', {"form": form})
      else:
          form = DocumentForm()

      return render(request, 'create_document.html', {"form": form})

@login_required(login_url="/login")
#@permission_required("base.add_confidential", login_url="/login", raise_exception=True)
def create_confidential(request):
      if request.method == 'POST':
          form = ConfidentialForm(request.POST, request.FILES)
          if form.is_valid():
            confidential = form.save(commit=False)
            confidential.author = request.user
            confidential.save()
            return redirect("/home")
          else:
            form = ConfidentialForm()

          return render(request, 'create_confidential.html', {"form": form})
      else:
          form = ConfidentialForm()

      return render(request, 'create_confidential.html', {"form": form})