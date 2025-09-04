from django.urls import path, include
from .views import authView, home, create_image, create_document, create_confidential, manage, verify, two_factor
from . import views

app_name = 'base'  # This helps with namespacing

urlpatterns = [
    path("", home, name="home"),  # This handles both /(EMPTY) and /home/ if you redirect
    path("home/", home, name="home"),  # Explicit /home/ path
    path("signup/", authView, name="signup"),
    path("create-post/", views.create_post, name="create_post"),
    path("image/", create_image, name="create_image"),
    path("documents/", create_document, name="create_document"),
    path("confidential/", create_confidential, name="create_confidential"),
    path("accounts/", include("django.contrib.auth.urls")),
    
    path("two_factor/", two_factor, name="two_factor"),
    path("verify/", verify, name="verify"),
    path("manage/", manage, name="manage"),
]