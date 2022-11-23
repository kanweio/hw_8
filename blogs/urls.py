from django.urls import path
from blogs.views import  blogs_view, hashtags_view
 

urlpatterns = [
    path('posts/', blogs_view),
    path('hashtags/', hashtags_view)
]