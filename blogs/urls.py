from django.urls import path
from blogs.views import PostCreateView, HashtagListView, PostDetailView, PostListVIew
 

urlpatterns = [
    path('posts/', PostListVIew.as_view()),
    path('hashtags/', HashtagListView.as_view()),
    path('posts/<int:id>/', PostDetailView.as_view()),
    path('posts/create/', PostCreateView.as_view())

]