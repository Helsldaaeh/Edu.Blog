from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from posts.forms import PostForm
from posts.models import Post
from django.contrib.auth.decorators import login_required


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
    if (post.author != request.user): return HttpResponseForbidden('Вы не имеете права')
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

    if (post.author != request.user): return HttpResponseForbidden('Вы не имеете права')

    if (request.method == 'POST'):
        post.delete()
        return redirect('posts')
    return render(request, 'posts/delete.html', {'post':post})


def about(request: HttpRequest) -> HttpResponse:
    return render(request, 'posts/about.html', {'title': 'About us'})

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
    return render(request, 'posts/login.html', {'form':form})

def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('login')
@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'posts/profile.html', {'user':request.user})

def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            author = request.user
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Пользователь с таким именем уже существует')
            else:
                User.objects.create_user(username=username, password=password)
                return redirect('users.login')
    else:
        form = UserForm()
    return render(request, 'users/register.html', {'form,':form})
#python manage.py makemigration
#python manage.py migrate
#python manage.py createsuperuser
#username: root
#password: root
#user = objects.create_user(username='some name', password='some password')
#user = objects.create_post(title='some title', text='some text', author = user)
