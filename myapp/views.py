from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from myapp.forms import LoginForm
from myapp.models import CustomUser, ChatRecord
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_http_methods
from django.core.files.base import ContentFile

@csrf_exempt
@require_http_methods(["POST"])
def post_data(request):
    try:
        data = json.loads(request.body)
        user_username = data.get('user')
        prompt = data.get('prompt')
        
        user = CustomUser.objects.get(username=user_username)

        # 處理圖片文件和圖片 URL
        response_image_url_1 = data.get('response_image_url_1')
        response_image_url_2 = data.get('response_image_url_2')
        response_image_url_3 = data.get('response_image_url_3')

        chat_record = ChatRecord(
            user=user,
            prompt=prompt,
            new_prompt='What are you in the mood for today?',  # 示例新提示
            response_text=json.dumps(['response_1', 'response_2', 'response_3']),  # 示例文本響應
            response_image_url_1=response_image_url_1,
            response_image_url_2=response_image_url_2,
            response_image_url_3=response_image_url_3,
            response_agree=True,  # 示例回答
            feedback='Good feedback'  # 示例反饋
        )
        chat_record.save()
        
        return JsonResponse({'status': 'Data received and saved successfully'})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

@require_http_methods(["GET"])
def get_data(request):
    user_username = request.GET.get('user')
    try:
        user = CustomUser.objects.get(username=user_username)
        chat_record = ChatRecord.objects.filter(user=user).last()

        data = {
            'user': user.username,
            'new_prompt': chat_record.new_prompt,
            'response_text': json.loads(chat_record.response_text),
            'response_image': [
                chat_record.response_image_url_1,
                chat_record.response_image_url_2,
                chat_record.response_image_url_3,
            ]
        }
        return JsonResponse(data)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except ChatRecord.DoesNotExist:
        return JsonResponse({'error': 'No chat record found'}, status=404)

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