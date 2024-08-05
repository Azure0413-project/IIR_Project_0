from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from myapp.forms import LoginForm
from myapp.models import CustomUser
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

@login_required
def index_page(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    
    users = CustomUser.objects.all()

    context = {
        'users': users,
    }
    
    return render(request, 'index.html', context)

def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("page")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

def register(request):
    registration_successful = False
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if not (username and password1 and password2):
            messages.error(request, "Please fill all the data!")
        elif CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
        elif password1 != password2:
            messages.error(request, "Passwords do not match!")
        else:
            CustomUser.objects.create(
                username=username,
                password=make_password(password1),
                last_login=timezone.now()
            )
            registration_successful = True
            messages.success(request, "Registration successful!")

    return render(request, 'register.html', {'registration_successful': registration_successful})