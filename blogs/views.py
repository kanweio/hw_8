from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime

from django.views.generic import ListView, CreateView, DetailView

from blogs import models

# Create your views here.
from blogs.models import Post, Comment, Hashtag
from blogs.forms import PostCreateForm, CommmentCreateForm
from users.utils import get_user_from_request

PAGINATION_LIMIT = 4


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
        search_text = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        if hashtag_id:
            posts = Post.objects.filter(hashtag=Hashtag.objects.get(id=hashtag_id))
        else:
            posts = Post.objects.all()

        if search_text:
            posts = posts.filter(title__startswith=search_text)

        max_page = round(posts.__len__() / PAGINATION_LIMIT)

        posts = posts[PAGINATION_LIMIT * (page - 1):PAGINATION_LIMIT * page]

        data = {
            'posts': posts,
            'user': get_user_from_request(request),
            'hashtag_id': hashtag_id,
            'current_page': page,
            'max_page': range(1, max_page + 1)
        }
        return render(request, 'post/posts.html', context=data)


def hello(request):
    if request.method == 'GET':
        return HttpResponse('Hello, its my project!')


def now_data(request):
    if request.method == 'GET':
        return HttpResponse(datetime.now())


def bye(request):
    if request.method == 'GET':
        return HttpResponse('Goodbye!')


class PostDetailView(DetailView, CreateView):
    model = Post
    template_name = 'post/detail.html'
    form_class = CommmentCreateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'comments': Comment.objects.filter(post_id=kwargs[self.object]),
            'post': self.object,
            'form': CommmentCreateForm,
            'user': get_user_from_request(self.request)

        }

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            self.model.objects.create(
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description')
            )
            return redirect(f'/posts/{kwargs["id"]}')
        else:
            return render(request, self.template_name, context=self.get_context_data(form=form), request=request)


class CreatePostAPIview(ListView, CreateView):
    model = Post
    template_name = 'post/create.html'
    form_class = PostCreateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'form': kwargs['form'] if kwargs.get('form') else self.form_class,
            'user': get_user_from_request(self.request)
        }

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            self.model.objects.create(
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                hashtags=form.cleaned_data.get('hashtag')
            )
            return redirect('/posts')
        else:
            return render(request, self.template_name, context=self.get_context_data(form=form))


class HashtagAPIview(ListView):
    model = Hashtag
    queryset = Hashtag.objects.all()
    template_name = 'hashtags/hashtags.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {
            'object_list': self.get_queryset(),
            'user': get_user_from_request(self.request)
        }
