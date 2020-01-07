from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Blog, BlogType, Comment

admin.site.register(CustomUser, UserAdmin)


class BlogAdmin(admin.ModelAdmin):
    pass


admin.site.register(Blog, BlogAdmin)

admin.site.register(BlogType)
