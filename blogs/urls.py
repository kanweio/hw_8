from django.urls import path
from blogs.views import  posts_view, hashtags_view, detail_view, main, create_posts_viev
 

urlpatterns = [
    path('posts/', posts_view),
    path('hashtags/', hashtags_view),
    path('posts/<int:id>/', detail_view),
    path('main/', main),
    path('posts/create', create_posts_viev)

]