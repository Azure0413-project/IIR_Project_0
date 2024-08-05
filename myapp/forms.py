from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from myapp.models import CustomUser
from myapp.models import Movie

class RegisterForm(UserCreationForm):
    user_age = forms.IntegerField(required=True, help_text="Required. Enter your age.")

    class Meta:
        model = CustomUser
        fields = ("username", "user_age", "password1", "password2")

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "password")

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['movie_name', 'description', 'image']