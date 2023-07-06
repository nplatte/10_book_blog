from django.contrib import admin
from django.urls import path, include
from login.views import login_page as login

urlpatterns = [
    path('', login, name='login_page')
]