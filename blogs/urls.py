from django.urls import path
from blogs.views import posts_view, HashtagAPIview, PostDetailView, main, CreatePostAPIview
 

urlpatterns = [
    path('posts/', posts_view),
    path('hashtags/', HashtagAPIview.as_view()),
    path('posts/<int:pk>/', PostDetailView.as_view()),
    path('main/', main),
    path('posts/create/', CreatePostAPIview.as_view())

]