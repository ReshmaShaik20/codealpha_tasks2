#from django.contrib import admin

# Register your models here.
# core/admin.py
from django.contrib import admin
from .models import User, Post, Comment, Like, Follow # Import our models!

# Register our models so they show up in the admin panel
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follow)
