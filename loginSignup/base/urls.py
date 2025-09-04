from django.urls import path, include
from .views import authView, home, create_post
from . import views

app_name = 'base'  # This helps with namespacing

urlpatterns = [
    path("", home, name="home"),  # This handles both / and /home/ if you redirect
    path("home/", home, name="home"),  # Explicit /home/ path
    path("signup/", authView, name="signup"),
    path("create-post/", views.create_post, name="create_post"),
    path("accounts/", include("django.contrib.auth.urls")),
]