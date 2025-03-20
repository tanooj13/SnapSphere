from django.contrib import admin

# Register your models here.
from .models import Profile, Snap, Like, Comment
admin.site.register(Profile)
admin.site.register(Snap) 
admin.site.register(Like)
admin.site.register(Comment)
