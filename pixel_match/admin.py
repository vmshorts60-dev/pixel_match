from django.contrib import admin
from .models import UserProfile, Interest, Match, Like, Message

admin.site.register(UserProfile)
admin.site.register(Interest)
admin.site.register(Match)
admin.site.register(Like)
admin.site.register(Message)
from .models import ProfilePhoto
admin.site.register(ProfilePhoto)
from django.contrib import admin

# Register your models here.
