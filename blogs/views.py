from django.shortcuts import render, redirect

from django.views import generic


# Create your views here.
from blogs.models import Post, Comment, Hashtag
from blogs.forms import PostCreateForm, CommmentCreateForm
from users.utils import get_user_from_request

PAGINATIONS_LIMIT = 4


class HashtagListView(generic.ListView):
    template_name = 'hashtags/hashtags.html'
    queryset = Hashtag.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'hashtags': self.get_queryset(),
            'user': get_user_from_request(self.request)
        }


class PostListVIew(generic.ListView):
    template_name = 'post/posts.html'
    queryset = Post.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        hashtag_id = self.request.GET.get('hashtag_id')
        search_text = self.request.GET.get('search')
        page = int(self.request.GET.get('page', 1))
        if hashtag_id:
            posts = Post.objects.filter(hashtag=Hashtag.objects.get(id=hashtag_id))
        else:
            posts = Post.objects.all()
        if search_text:
            posts = posts.filter(title__icontains=search_text)

        max_page = round(posts.__len__() / PAGINATIONS_LIMIT)
        posts = posts[PAGINATIONS_LIMIT * (page - 1):PAGINATIONS_LIMIT * page]
        return {
            'posts': posts,
            'user': get_user_from_request(self.request),
            'current_page': page,
            'max_page': list(range(1, max_page + 1)),
            'hashtag_id': hashtag_id,
            'search_text': search_text
        }


class PostDetailView(generic.DetailView, generic.CreateView):
    form_class = CommmentCreateForm
    template_name = 'post/detail.html'
    queryset = Post.objects.all()
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        return {
            'post': self.get_object(),
            'comments': Comment.objects.filter(post=self.get_object()),
            'form': kwargs.get('form', self.form_class),
            'user': get_user_from_request(self.request)
        }

    def post(self, request, *args, **kwargs):
        form = CommmentCreateForm(data=request.POST)

        if form.is_valid():
            Comment.objects.create(
                author=request.user,
                text=form.cleaned_data.get('text'),
                post_id=self.get_object().id
            )
            return redirect(f'/posts/{self.get_object().id}/')
        return render(request, self.template_name, context=self.get_context_data(form=form))


class PostCreateView(generic.CreateView):
    form_class = PostCreateForm
    template_name = 'post/create.html'

    def get_context_data(self, **kwargs):
        return {
            'form': kwargs.get('form', self.form_class),
            'user': get_user_from_request(self.request)
        }

    def post(self, request, *args, **kwargs):
        form = PostCreateForm(data=request.POST)
        if form.is_valid():
            Post.objects.create(
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description')
            )
            return redirect('/posts/')
        else:
            data = {
                'form': form,
                'user': get_user_from_request(request)
            }
            return render(request, self.template_name, self.get_context_data(form=form))
