from django.urls import path
from blogs.views import PostListVIew, HashtagListView, PostDetailView, PostCreateView
 

urlpatterns = [
    path('posts/', PostListVIew.as_view()),
    path('hashtags/', HashtagListView.as_view()),
    path('posts/<int:pk>/', PostDetailView.as_view()),
    path('posts/create/', PostCreateView.as_view())

]
