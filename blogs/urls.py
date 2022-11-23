from django.urls import path
from blogs.views import  posts_view, hashtags_view, detail_view, main
 

urlpatterns = [
    path('posts/', posts_view),
    path('hashtags/', hashtags_view),
    path('posts/<int:id>/', detail_view),
    path('main/',main)

]