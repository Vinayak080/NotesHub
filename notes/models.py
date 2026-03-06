#from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='notes/')
    tags = models.JSONField(default=list)  # Works well with MongoDB
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    download_count = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username}"
