from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.views.generic import View
from django.http import HttpResponse

from .models import Post, Comment
from .forms import PostForm, LoginForm, CommentForm


def post_list(request):
    print("post_list")
    if request.GET.get("item"):
        option= request.GET.get('fd_name')
        search_type='contains'
        filter = option + '__' + search_type
        posts = Post.objects.filter(**{filter: request.GET.get('item')}, published_date__lte = timezone.now()).order_by('-published_date')
        return render(request, 'blog/post_list.html',{'posts':posts})

    posts = Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html',{'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk) # 위의 4줄과 같은 역할
    comments = Comment.objects.filter(created_date__lte = timezone.now(), post=post).order_by('-created_date')
    
    if request.method =="POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {
            'post':post,
            'comments':comments,
            'form':form
        })

#로그인 요구를 위한 장식자
@login_required(login_url='admin:login')
def post_new(request):
    if request.method =='POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()

            return redirect('post_detail', post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form':form})

@login_required(login_url='admin:login')
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form  =  PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk = post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html',{'form':form})

def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts':posts})

def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog:post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form  = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html',{'form':form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail',pk=comment.post.pk)

    
    
