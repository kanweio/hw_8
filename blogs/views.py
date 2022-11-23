from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from blogs import models

# Create your views here.
from blogs.models import Post, Comment, Hashtag


def main(request):
    if request.method == 'GET':
        posts = models.Post.objects.all()

        data = {
            'post': posts
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
            'posts': posts
        }
        return render(request, 'post/posts.html', context=context)


def hashtags_view(request):
    if request.method == 'GET':
        hashtags = models.Hashtag.objects.all()

        data = {
            'hashtags': hashtags
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
            'comments': comments
        }

        return render(request, 'post/detail.html', context=data)
