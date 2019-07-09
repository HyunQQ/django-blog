from django.conf import settings
from django.db import models
from django.utils import timezone

#모델의 정의
class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE,)
    # author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=200)
    text = models.TextField()
    category = models.CharField(max_length=200)
    created_date = models.DateTimeField(default = timezone.now)
    published_date = models.DateTimeField(blank = True, null=True)
    
    def __str__(self):
        return self.title

    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def approved_comment(self):
        return self.comments.filter(approved_comment=True)
    
class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE,)
    author = models.CharField(max_length = 200)
    text = models.TextField()
    created_date = models.DateTimeField(default = timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text