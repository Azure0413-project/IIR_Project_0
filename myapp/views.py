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
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from final import RDS
from PIL import Image
from io import BytesIO
import base64

@csrf_exempt
def get_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user')
            prompt = data.get('prompt')

            new_prompt, restaurant_name, food_name, food_price, image_1, image_2, image_3, response_image_url_1, response_image_url_2, response_image_url_3, google_map = RDS(prompt)

            def image_to_bytes(image):
                byte_io = BytesIO()
                image.save(byte_io, format='PNG')  # Save as PNG or another format if needed
                return byte_io.getvalue()

            image_1_bytes = image_to_bytes(image_1)
            image_2_bytes = image_to_bytes(image_2)
            image_3_bytes = image_to_bytes(image_3)

            try:
                user = CustomUser.objects.get(id=user_id)
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

            chat_record = ChatRecord.objects.create(
                user=user,
                prompt=prompt,
                new_prompt=new_prompt,
                restaurant_name=restaurant_name,
                food_name=food_name,
                food_price=food_price,
                response_text=None,
                google_map=google_map,
                response_image_1=image_1_bytes,
                response_image_2=image_2_bytes,
                response_image_3=image_3_bytes,
                response_image_url_1=response_image_url_1,
                response_image_url_2=response_image_url_2,
                response_image_url_3=response_image_url_3,
                response_agree=None,  # 暫時設置為 None
                feedback=None  # 暫時設置為 None
            )

            return JsonResponse({
                'record_id': chat_record.id,
                'new_prompt': new_prompt,
                'restaurant_name': restaurant_name,
                'food_name': food_name,
                'food_price': food_price,
                'response_text': None,
                'image_1': base64.b64encode(image_1_bytes).decode('utf-8'),
                'image_2': base64.b64encode(image_2_bytes).decode('utf-8'),
                'image_3': base64.b64encode(image_3_bytes).decode('utf-8'),
                'image_url_1': response_image_url_1,
                'image_url_2': response_image_url_2,
                'image_url_3': response_image_url_3,
                'google_map': google_map
            })
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def store_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            record_id = data.get('record_id')
            response_agree = data.get('response_agree')
            feedback = data.get('feedback')

            try:
                chat_record = ChatRecord.objects.get(id=record_id)
                chat_record.response_agree = response_agree
                chat_record.feedback = feedback
                chat_record.save()
                
                return JsonResponse({'status': 'success'})
            
            except ChatRecord.DoesNotExist:
                return JsonResponse({'error': 'Record not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
            
@login_required
def index_page(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    

    users = CustomUser.objects.all()
    user_id = request.user.id

    context = {
        'current_user': users,
        'user_id' : user_id,
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