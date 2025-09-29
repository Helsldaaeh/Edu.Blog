from django.shortcuts import redirect
from django.urls import path
from django.contrib.auth import views as auth_views
from posts import views

path('users/register/', views.register_view, name='users.register'),
path('users/login/', views.login_view, name='users.login'),
path('users/logout/', views.logout_view, name='users.logout'),
path('users/profile/', views.profile_view, name='users.profile'),