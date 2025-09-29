from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from posts.forms import PostForm
from posts.models import Post
from forms import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UserForm(request.Post)
        if form.is_valid():
            username = form.cleaned_data('username')
            password = form.cleaned_data('password')
            user = authenticate(
                request,
                username=username,
                password=password,
            )
            if user is not None:
                login(request, user)
                return redirect('posts')
            else:
                messages.error(request, 'Не верное имя пользователя, или пароль')
    else:
        form = UserForm()
    return render(request, 'users/login.html', {'form':form})

def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('login')

@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'users/profile.html', {'user':request.user})

def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Пользователь с таким именем уже существует')
            else:
                User.objects.create_user(username=username, password=password)
                return redirect('users.login')
    else:
        form = UserForm()
    return render(request, 'users/register.html', {'form,':form})