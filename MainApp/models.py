from django.db import models
from django.db.models import ForeignKey


# Create your models here.

class Attachment(models.Model):
    message = models.ForeignKey('Message', on_delete=models.CASCADE)
    file = models.FileField(upload_to='user-attachments/')

    def extension(self):
        return self.file.name.split('.')[-1]

class Message(models.Model):
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, default=1, related_name="messages")
    text = models.TextField()


class Chat(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title