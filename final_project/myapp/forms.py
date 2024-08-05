from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from myapp.models import CustomUser

class RegisterForm(UserCreationForm):
    user_age = forms.IntegerField(required=True, help_text="Required. Enter your age.")

    class Meta:
        model = CustomUser
        fields = ("username", "password1", "password2")
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists. Please choose another one.")
        return username

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "password")

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
