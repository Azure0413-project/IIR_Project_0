from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from myapp.forms import RegisterForm, LoginForm, MovieForm
from myapp.models import CustomUser, Movie, Rating

# Create your views here.
def hello_view(request):
    return render(request, 'hello.html', {
    'data': "Hello world ",
    })

def happy_view(request):
    return render(request, 'happy.html', {
    'data': "I am very happy to be able to join the IIR laboratory.",
    })

def get_movie_name(request, movie_name):
    return HttpResponse("Get movie name: " + movie_name)

def get_name(request, name):
    return HttpResponse("My name is: " + name + "<br> I am very happy to be able to join the IIR laboratory.")

def get_user_name(request, name):
    context = {'name': name}
    return render(request, 'img.html', context)

from myapp.models import Movie
from myapp.models import User
from myapp.models import Rating

def save_data_into_db(request, movie_name):
    m = Movie(movie_name = movie_name)
    m.save()
    return HttpResponse(movie_name + " is in database now!")

def get_all_data(request):
    all_movies = Movie.objects.all()
    for movie in all_movies:
        print(movie.movie_name)
    return HttpResponse('Get all movies in database!')

def get_all_data(request):
    all_movies = Movie.objects.all()
    return render(request, 'main.html', {'movies': all_movies})

def add_user(request, name, age):
    user = User(user_name=name, user_age=age)
    user.save()
    return HttpResponse(f"User {name} added with age {age}.")

def get_all_user(request):
    users = User.objects.all()
    return render(request, 'main.html', {'users': users})

def post_movie_name(request):
    if request.method == 'POST':
        movie_name = request.POST.get('movie name')
        if movie_name:
            m = Movie(movie_name=movie_name)
            m.save()
            return redirect('show_movie_name', movie_name=movie_name)
        else:
            return HttpResponse("No movie name provided.")
    return render(request, 'add.html')

def show_movie_name(request, movie_name):
    return render(request, 'show_input.html', {'movie_name': movie_name})

def index_page(request):
    search_query = request.GET.get('search', '')
    movies = Movie.objects.filter(movie_name__icontains=search_query)
    users = User.objects.all()
    ratings = Rating.objects.all()

    context = {
        'movies': movies,
        'users': users,
        'ratings': ratings
    }
    
    return render(request, 'index.html', context)

# new
def add_view(request):
    return render(request, 'add.html')

def insert_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            form.save()  # Save the movie using the form
            return redirect('index_page')
    else:
        form = MovieForm()
    return render(request, 'add.html', {'form': form})

def update_movie(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        movie_name = request.POST.get('movie_name')
        movie_description = request.POST.get('movie_description')
        movie_image = request.FILES.get('movie_image')
        
        if movie_id and movie_name and movie_description:
            movie = get_object_or_404(Movie, id=movie_id)
            movie.movie_name = movie_name
            movie.movie_description = movie_description
            
            if movie_image:
                movie.movie_image = movie_image
            
            movie.save()
            return redirect('index_page')
    return render(request, 'add.html')

def delete_movie(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        if movie_id:
            movie = get_object_or_404(Movie, id=movie_id)
            movie.delete()
            return redirect('index_page')
    return render(request, 'add.html')

def insert_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_age = request.POST.get('user_age')
        is_admin = request.POST.get('is_admin') == 'on'
        
        if user_id and username and password and user_age:
            User.objects.create(
                id=user_id,
                username=username,
                password=password,  # Password should be hashed in practice
                user_age=user_age,
                is_admin=is_admin
            )
            return redirect('index_page')
    return render(request, 'add.html')

def update_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_age = request.POST.get('user_age')
        is_admin = request.POST.get('is_admin') == 'on'
        
        if user_id and username and user_age:
            user = get_object_or_404(User, id=user_id)
            user.username = username
            
            if password:
                user.set_password(password)  # Properly hash the password
            user.user_age = user_age
            user.is_admin = is_admin
            user.save()
            return redirect('index_page')
    return render(request, 'add.html')

def delete_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if user_id:
            user = get_object_or_404(User, id=user_id)
            user.delete()
            return redirect('index_page')
    return render(request, 'add.html')

def insert_rating(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        movie_id = request.POST.get('movie_id')
        rating_value = request.POST.get('rating')
        
        if user_id and movie_id and rating_value:
            user = get_object_or_404(User, id=user_id)
            movie = get_object_or_404(Movie, id=movie_id)
            Rating.objects.create(
                user=user,
                movie=movie,
                rating=rating_value
            )
            return redirect('index_page')
    return render(request, 'add.html')

def update_rating(request):
    if request.method == 'POST':
        rating_id = request.POST.get('rating_id')
        user_id = request.POST.get('user_id')
        movie_id = request.POST.get('movie_id')
        rating_value = request.POST.get('rating')
        
        if rating_id and user_id and movie_id and rating_value:
            rating = get_object_or_404(Rating, id=rating_id)
            user = get_object_or_404(User, id=user_id)
            movie = get_object_or_404(Movie, id=movie_id)
            rating.user = user
            rating.movie = movie
            rating.rating = rating_value
            rating.save()
            return redirect('index_page')
    return render(request, 'add.html')

def delete_rating(request):
    if request.method == 'POST':
        rating_id = request.POST.get('rating_id')
        if rating_id:
            rating = get_object_or_404(Rating, id=rating_id)
            rating.delete()
            return redirect('index_page')
    return render(request, 'add.html')

def page(request):
    search_query = request.GET.get('search', '')
    movies = Movie.objects.filter(movie_name__icontains=search_query)
    users = User.objects.all()
    ratings = Rating.objects.all()

    context = {
        'movies': movies,
        'users': users,
        'ratings': ratings
    }
    
    return render(request, 'app.html', context)

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("page")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

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
        form = LoginForm()
    return render(request, "login.html", {"form": form})