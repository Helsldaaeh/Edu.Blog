from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from posts.forms import PostForm
from posts.models import Post
from forms import UserForm


def post(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.all()
    return render(request, 'posts/posts.html', {'title': 'Posts', 'posts': posts})


def create(request: HttpRequest) -> HttpResponseRedirect | HttpResponse | None:
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = Post(title=form.cleaned_data['title'], content=form.cleaned_data['title'])
            post.save()
            return redirect('post-list')
        else:
            return render(request, 'posts/create_post.html', {'error': 'Все поля обязательные'})

    form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


def retrieve(request: HttpRequest, post_id:int) -> HttpResponse:
    post = Post.objects.get(pk=post_id)
    return render(request, 'posts/retrieve.html', {'post':post})

def update(request: HttpRequest, post_id:int) -> HttpResponse:
    post = get_object_or_404(Post, id=post_id)
    if (request.method == 'POST'):
        form = PostForm(request.POST)
        if (form.is_valid()):
            post.title = form.cleaned_data('title')
            post.content = form.cleaned_data('content')
            post.save()
            return redirect('posts')
    else:
        form = PostForm(initial={
            'title':post.title,
            'content':post.content,
        })
    return render(request, 'posts/update.html', {'form':form, 'post':post})

def delete(request:HttpRequest, post_id:int) -> HttpResponse:
    post = get_object_or_404(Post, id=post_id)
    if (request.method == 'POST'):
        post.delete()
        return redirect('posts')
    return render(request, 'posts/delete.html', {'post':post})


def about(request: HttpRequest) -> HttpResponse:
    return render(request, 'posts/about.html', {'title': 'About us'})

def login(request: HttpRequest) -> HttpResponse:
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
    return render(request, 'posts/login.html', {'form':form})
