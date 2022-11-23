from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from blogs import models

# Create your views here.
from blogs.models import Post


def main(request):
    if request.method == 'GET':
        posts = models.Post.objects.all()

        data = {
            'post': posts
        }
        return render(request, 'layouts/main.html', context=data)


def blogs_view(request):
    if request.method == 'GET':
        posts = models.Post.objects.all()

        data = {
            'posts': posts
        }

        return render(request, 'post/posts.html', context=data)


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


def detail_view(request, **kwargs):
    if request.method == 'GET':
        post = Post.objects.get(id=kwargs['id'])
        data = {
            'post': post
        }

        return render(request, 'post/detail.html', context=data)


def now_data(request):
    if request.method == 'GET':
        return HttpResponse(datetime.now())


def bye(request):
    if request.method == 'GET':
        return HttpResponse('Goodbye!')
