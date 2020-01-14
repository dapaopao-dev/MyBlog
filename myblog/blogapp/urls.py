# coding: utf-8

from django.urls import path
from .views import Index, Login, BlogView, BlogDetails, PhotoView, RegisterUser, LogoutUser, MyCenter, BlogPublish, \
    UpdateBlog

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('login', Login.as_view(), name='login'),
    path('logout', LogoutUser.as_view(), name='logout'),
    path('bloglist', BlogView.as_view(), name='blog_list'),
    path('blogdetails/<int:blog_id>', BlogDetails.as_view(), name='blog_details'),
    path('photo', PhotoView.as_view(), name='photo'),
    path('register', RegisterUser.as_view(), name='register'),
    path('mycenter', MyCenter.as_view(), name='my_center'),
    path('blogpublish', BlogPublish.as_view(), name='blog_publish'),
    path('mycenter/updateblog/<int:update_blog_id>', UpdateBlog.as_view(), name='update_blog')
]
