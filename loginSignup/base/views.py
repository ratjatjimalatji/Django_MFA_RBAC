from urllib import request
from .forms import RegisterForm, PostForm, ImageForm, DocumentForm, ConfidentialForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login
from django.contrib import messages
from .models import Post, Image, Document, ConfidentialFile

@login_required(login_url="/login")
def home(request):
    posts = Post.objects.all()
    images = Image.objects.all()  
    documents = Document.objects.all()  
    confidential_files = ConfidentialFile.objects.all()  

    if request.method == "POST":
        post_id = request.POST.get("post-id")
        image_id = request.POST.get("image-id")  # Add this
        document_id = request.POST.get("document-id")  # Add this
        confidential_id = request.POST.get("confidential-id")  # Add this
        
        #Deleting a post
        if post_id:
          post = Post.objects.filter(id=post_id).first()
          if post and (post.author == request.user or request.user.has_perm("base.delete_post")):
            post.delete()
        print(post_id)

        # Delete document
        if document_id:
            document = Document.objects.filter(id=document_id).first()
            if document and (document.author == request.user or request.user.has_perm("base.delete_document")):
                document.delete()

        # Delete image
        if image_id:
            image = Image.objects.filter(id=image_id).first()
            if image and (image.author == request.user or request.user.has_perm("base.delete_image")):
                image.delete()

        # Delete confidential file
        if confidential_id:
            confidential = ConfidentialFile.objects.filter(id=confidential_id).first()
            if confidential and (confidential.author == request.user or request.user.has_perm("base.delete_confidentialfile")):
                confidential.delete()

    return render(request, "home.html", {
        "posts": posts,
        "images": images,
        "documents": documents,
        "confidential_files": confidential_files
    })

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
@permission_required("base.add_image", login_url="/login", raise_exception=True)
def create_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.author = request.user
            image.save()
            messages.success(request, 'Image uploaded successfully!')
            return redirect("/home")
        else:
            # Add this to debug what's wrong
            messages.error(request, 'Please fix the errors below.')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ImageForm()

    return render(request, 'create_image.html', {"form": form})

@login_required
def edit_image_file(request, image_id):
    # CRITICAL FIX: You were getting ConfidentialFile instead of Image
    image_file = get_object_or_404(Image, pk=image_id)
    
    # Check if the user is the author or an admin
    if request.user != image_file.author and not request.user.is_staff:
        messages.error(request, "You don't have permission to edit this file.")
        return redirect('base:home')

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES, instance=image_file) # Added request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, 'Image file updated successfully!')
            return redirect('base:home') 
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ImageForm(instance=image_file)
    
    return render(request, 'edit_image.html', {'form': form, 'image': image_file})


@login_required(login_url="/login")
@permission_required("base.add_document", login_url="/login", raise_exception=True)
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

@login_required
def edit_document_file(request, document_id):
    document_file = get_object_or_404(Document, pk=document_id)
    
    if request.user != document_file.author and not request.user.is_staff:
        messages.error(request, "You don't have permission to edit this file.")
        return redirect('base:home')

    if request.method == 'POST':
        # Added request.FILES for handling document uploads
        form = DocumentForm(request.POST, request.FILES, instance=document_file)
        if form.is_valid():
            form.save()
            messages.success(request, 'Document file updated successfully!')
            return redirect('base:home') 
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = DocumentForm(instance=document_file)
    
    return render(request, 'edit_document.html', {'form': form, 'document': document_file})

@login_required(login_url="/login")
@permission_required("base.add_confidentialfile", login_url="/login", raise_exception=True)
def create_confidential(request):
    if request.method == 'POST':
        form = ConfidentialForm(request.POST)
        if form.is_valid():
            confidential = form.save(commit=False)
            confidential.author = request.user
            confidential.save()
            messages.success(request, 'Confidential file created successfully!')
            return redirect("base:home")
        else:
            messages.error(request, 'Please fix the errors below.')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ConfidentialForm()

    return render(request, 'create_confidential.html', {"form": form})

@login_required
def edit_confidential_file(request, confidential_id):
    confidential_file = get_object_or_404(ConfidentialFile, pk=confidential_id)
    
    # Check if the user is the author or an admin
    if request.user != confidential_file.author and not request.user.is_staff:
        messages.error(request, "You don't have permission to edit this file.")
        return redirect('base:home')

    if request.method == 'POST':
        form = ConfidentialForm(request.POST, instance=confidential_file)
        if form.is_valid():
            form.save()
            messages.success(request, 'Confidential file updated successfully!')
            return redirect('base:home') 
    else:
        form = ConfidentialForm(instance=confidential_file)
    
    return render(request, 'edit_confidential.html', {'form': form, 'confidential': confidential_file})