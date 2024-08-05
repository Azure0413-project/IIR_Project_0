from django.contrib import admin
from myapp.models import User, Movie, Rating, CustomUser
from django.contrib.auth.admin import UserAdmin

# admin.site.register(User)
# admin.site.register(Movie)
# admin.site.register(Rating)

admin.site.register(CustomUser)
admin.site.register(Movie)
admin.site.register(Rating)