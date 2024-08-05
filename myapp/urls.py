from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.index_page), name='page'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
]