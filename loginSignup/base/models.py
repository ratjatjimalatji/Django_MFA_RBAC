from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    
    # New fields for uploads
    text_content = models.TextField(blank=True, null=True)
    document = models.FileField(upload_to='documents/', blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title