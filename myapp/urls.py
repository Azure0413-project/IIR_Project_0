from . import views
from django.urls import path
urlpatterns = [
    path('helloworld',views.hello_view),
    path('happy',views.happy_view),
    path('name/<str:movie_name>/', views.get_movie_name, name='get_movie_name'),
    path('happyjoin/<str:name>/', views.get_name, name='get_name'),
    path('pichappyjoin/<str:name>/', views.get_user_name, name='get_user_name'),
    path('add_movie/<str:movie_name>/', views.save_data_into_db, name='save_data_into_db'),
    path('get_all_data/', views.get_all_data, name='get_all_data'),
    path('add_user/<str:name>/<int:age>/', views.add_user, name='add_user'),
    path('get_all_user/', views.get_all_user, name='get_all_user'),
    path('post_movie_name', views.post_movie_name, name='post_movie_name'),
    path('show_movie_name/<str:movie_name>/', views.show_movie_name, name='show_movie_name'),
    path('admin', views.index_page, name='index_page'),
    path('add/', views.add_view, name='add_view'),
    path('', views.page, name='page'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    # Movie management
    path('insert_movie/', views.insert_movie, name='insert_movie'),
    path('update_movie/', views.update_movie, name='update_movie'),
    path('delete_movie/', views.delete_movie, name='delete_movie'),

    # User management
    path('insert_user/', views.insert_user, name='insert_user'),
    path('update_user/', views.update_user, name='update_user'),
    path('delete_user/', views.delete_user, name='delete_user'),

    # Rating management
    path('insert_rating/', views.insert_rating, name='insert_rating'),
    path('update_rating/', views.update_rating, name='update_rating'),
    path('delete_rating/', views.delete_rating, name='delete_rating'),
]