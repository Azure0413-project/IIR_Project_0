from django.contrib import admin
from myapp.models import CustomUser, ChatRecord

admin.site.register(CustomUser)
admin.site.register(ChatRecord)