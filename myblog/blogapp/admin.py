from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Blog, BlogType, Comment

admin.site.register(CustomUser, UserAdmin)


admin.site.register(Blog)

admin.site.register(BlogType)

admin.site.register(Comment)
