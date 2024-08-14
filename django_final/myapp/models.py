from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Custom user model with username and password
    pass

class ChatRecord(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='chat_records')
    prompt = models.TextField()
    new_prompt = models.TextField()
    
    restaurant_name = models.TextField()
    food_name = models.TextField()
    food_price = models.TextField()
    response_text = models.TextField()
    google_map = models.TextField()
    
    response_image_1 = models.ImageField(upload_to='responses/', null=True, blank=True)
    response_image_2 = models.ImageField(upload_to='responses/', null=True, blank=True)
    response_image_3 = models.ImageField(upload_to='responses/', null=True, blank=True)
    response_image_url_1 = models.URLField(null=True, blank=True)
    response_image_url_2 = models.URLField(null=True, blank=True)
    response_image_url_3 = models.URLField(null=True, blank=True)

    
    response_agree = models.BooleanField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.prompt[:50]}'