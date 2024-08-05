from unicodedata import name
from django.db import models
from django.contrib.auth.models import AbstractUser
import myapp

class User(models.Model):
    id = models.AutoField(primary_key=True)
    user_age = models.IntegerField()
    user_name = models.CharField(max_length=50)

class CustomUser(AbstractUser):
    user_age = models.IntegerField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.username == 'admin':
            self.is_admin = True
        super().save(*args, **kwargs)

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    movie_name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='movies/', blank=True, null=True)

class Rating(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField()