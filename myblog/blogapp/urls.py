# coding: utf-8

from django.urls import path
from .views import Index, Login, BlogView, BlogDetails, PhotoView, RegisterUser

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('login', Login.as_view(), name='login'),
    path('bloglist', BlogView.as_view(), name='blog_list'),
    path('blogdetails', BlogDetails.as_view(), name='blog_details'),
    path('photo', PhotoView.as_view(), name='photo'),
    path('register', RegisterUser.as_view(), name='register')
]
