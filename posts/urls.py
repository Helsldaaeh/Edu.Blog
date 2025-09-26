from django.shortcuts import redirect
from django.urls import path
from django.contrib.auth import views as auth_views
from posts import views

urlpatterns = [
    path('post/', views.post, name='post-list'),
    path('post/<int:post_id>', views.retrieve, name="retrieve"),
    path('post/<int:post_id>/update', views.update, name="update"),
    path('post/<int:post_id>/delete/', views.delete, name="delete"),
    path('post/create', views.create, name='post-create'),
    path('login/', views.login, name='login'),
    path('about/', views.about, name='about'),
    #path('login/', auth_views.LoginView.as_view(template_name='posts/login.hrml'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]