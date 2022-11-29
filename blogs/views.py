from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from blogs import models

# Create your views here.
from blogs.models import Post, Comment, Hashtag
from blogs.forms import PostCreateForm, CommmentCreateForm
from users.utils import get_user_from_request


def main(request):
    if request.method == 'GET':
        posts = models.Post.objects.all()

        data = {
            'post': posts,
            'user': get_user_from_request(request)
        }
        return render(request, 'layouts/main.html', context=data)


def posts_view(request):
    if request.method == 'GET':
        hashtag_id = request.GET.get('hashtag_id')
        if hashtag_id:
            posts = Post.objects.filter(hashtag=Hashtag.objects.get(id=hashtag_id))
        else:
            posts = Post.objects.all()
        context = {
            'posts': posts,
            'user': get_user_from_request(request)
        }
        return render(request, 'post/posts.html', context=context)


def hashtags_view(request):
    if request.method == 'GET':
        hashtags = models.Hashtag.objects.all()

        data = {
            'hashtags': hashtags,
            'user': get_user_from_request(request)
        }

        return render(request, 'hashtags/hashtags.html', context=data)


def hello(request):
    if request.method == 'GET':
        return HttpResponse('Hello, its my project!')


def now_data(request):
    if request.method == 'GET':
        return HttpResponse(datetime.now())


def bye(request):
    if request.method == 'GET':
        return HttpResponse('Goodbye!')


def detail_view(request, **kwargs):
    if request.method == 'GET':
        post = Post.objects.get(id=kwargs['id'])
        hashtag = Hashtag.objects.filter(posts=post)
        comments = Comment.objects.filter(post=post)

        data = {
            'post': post,
            'hashtag': hashtag,
            'comments': comments,
            'form': CommmentCreateForm,
            'user': get_user_from_request(request)
        }
        return render(request, 'post/detail.html', context=data)

    if request.method == 'POST':
        form = CommmentCreateForm(data=request.POST)
        if form.is_valid():
            Comment.objects.create(
                author_id=1,
                text=form.cleaned_data.get('text'),
                post_id=kwargs['id']
                )
            return redirect(f'/posts/{kwargs["id"]}')
        else:
            post = Post.objects.get(id=kwargs['id']),
            comments = Comment.objects.filter(post=post)
            data = {
                'comments': comments,
                'post': post,
                'form': form,
                'user': get_user_from_request(request)

            }
            return render(request, 'post/detail.html', context=data)


def create_posts_viev(request):
    if request.method == 'GET':
        data = {
            'forms': PostCreateForm,
            'user': get_user_from_request(request)
        }
        return render(request, 'post/create.html', context=data)

    if request.method == 'POST':
        form = PostCreateForm(data=request.POST)

        if form.is_valid():
            post = Post.objects.create(
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                hashtags=form.cleaned_data.get('hashtag')
            )
            return redirect(f'/posts/{post.id}')
        else:
            data = {
                'form': form,
                'user': get_user_from_request(request)
            }
            return render(request, 'post/create.html', context=data)
