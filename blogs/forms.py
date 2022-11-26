from django import forms
from blogs.models import Hashtag

HASHTAG_CHOICES = (
    (hashtag.id, hashtag.title) for hashtag in Hashtag.objects.all()
)


class PostCreateForm(forms.Form):
    title = forms.CharField(max_length=100, min_length=5)
    description = forms.CharField(widget=forms.Textarea)
    hashtag = forms.ChoiceField


class CommmentCreateForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label='Оставьте комментарий!')
