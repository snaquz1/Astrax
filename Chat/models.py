import secrets
from datetime import datetime

from django.db import models
from django.db.models import ForeignKey
from Users.models import CustomUser

# Create your models here.

class Attachment(models.Model):
    message = models.ForeignKey('Message', on_delete=models.CASCADE)
    file = models.FileField(upload_to='user-attachments/')
    ext = models.CharField(max_length=10, default='.txt')

    def extension(self):
        return self.file.name.split('.')[-1]

class Message(models.Model):
    username = models.ForeignKey("Users.CustomUser", on_delete=models.CASCADE, related_name="users", default=1)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, default=1, related_name="messages")
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class ChatMember(models.Model):
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)
    user = models.ForeignKey('Users.CustomUser', on_delete=models.CASCADE)
    role = models.CharField('Role', default="member")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('chat', 'user')


class Chat(models.Model):
    members = models.ManyToManyField(CustomUser, through=ChatMember)
    title = models.CharField(max_length=100)
    invite_token = models.CharField(max_length=100, default=secrets.token_urlsafe(10))


    def __str__(self):
        return self.title


