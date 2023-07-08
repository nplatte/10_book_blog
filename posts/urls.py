from django.contrib import admin
from django.urls import path, include
from posts.views import create_post_page, view_post_page

urlpatterns = [
    path('create-post', create_post_page, name='create_post'),
    path('view-post', view_post_page, name='view_post')
]