from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    # with username and password
    pass

class ChatRecord(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='chat_records')
    prompt = models.TextField()
    response_text = models.TextField()
    response_image = models.ImageField(upload_to='responses/', null=True, blank=True)
    response_agree = models.BooleanField()
    feedback = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.prompt[:50]}'