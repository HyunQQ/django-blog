from django import forms
from django.contrib.auth.models import User

from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        
        model = Post
        # fields = '__all__' 모든 필드 사용시
        fields =('title','text','category')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({
            'class':'form-control click2edit',
            'id':'summernote',
            })



class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        password = forms.CharField(widget=forms.PasswordInput)
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class':'fadeIn signin',
            'id':'login',
            'placeholder':'ID',
        })
        self.fields['password'].widget.attrs.update({
            'class':'fadeIn signin',
            'id':'password',
            'placeholder':'PW',
        })

# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['text','author']

#         # 파일 업로드 필드에 제한 및 클래스, 라벨 추가
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['text'].widget.attrs.update({
#             'class':'form-control',
#         })
#         self.fields['author'].widget.attrs.update({
#             'class':'form-control',
#         })



# class SearchForm(forms.ModelForm):
#     class Meta:
#         model = Search
#         filed = ['word']
#     # word = forms.CharField(label='Search word')
