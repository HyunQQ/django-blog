from django import forms
from django.contrib.auth.models import User

from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = '__all__' 모든 필드 사용시
        fields =('title','text','category')


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text','author']

# class SearchForm(forms.ModelForm):
#     class Meta:
#         model = Search
#         filed = ['word']
#     # word = forms.CharField(label='Search word')
