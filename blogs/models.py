from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Hashtag(models.Model):
    text = models.TextField()
    posts = models.ManyToManyField('Post')

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)


class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    hashtags = models.ForeignKey(Hashtag, on_delete=models.CASCADE, null=True,
                                 related_name="Post")

    def __str__(self):
        return self.title
