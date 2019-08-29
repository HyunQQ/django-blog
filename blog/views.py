import pandas as pd

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.views.generic import View
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Min

from .models import Post, Comment, Post_img
from .forms import PostForm, LoginForm, CommentForm
from .utils.function import remove_html_tag

def post_list(request):
    
    if request.GET.get("item"):
        option= request.GET.get('fd_name')
        search_type='contains'
        filter = option + '__' + search_type
        
        posts = Post.objects.filter(**{filter: request.GET.get('item')}, published_date__lte = timezone.now()).order_by('-published_date')
        posts_for_category = Post.objects.exclude(title__exact='').values('category').order_by('-published_date')
        tmp_posts_for_category = posts_for_category.values('category')
        category_lst = pd.unique(pd.DataFrame.from_records(tmp_posts_for_category)['category'])

        ###############paging #################
        paginator = Paginator(posts,5)
        page = request.GET.get('page')
        posts = paginator.get_page(page)

        return render(request, 'blog/post_list.html',{
            'posts':posts,
            'posts_for_category':category_lst,
        })
    posts_for_category = Post.objects.exclude(title__exact='').values('category').order_by('-published_date')
    posts = Post.objects.exclude(title__exact='').filter( published_date__lte = timezone.now()).order_by('-published_date')
    tmp_posts_for_category = posts_for_category.values('category')
    category_lst = pd.unique(pd.DataFrame.from_records(tmp_posts_for_category)['category'])
    
    ###############paging #################
    paginator = Paginator(posts,5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'blog/post_list.html',{
            'posts':posts,
            'posts_for_category':category_lst
        })

def post_category_list(request, category):
    
    posts_for_category = Post.objects.exclude(title__exact='').values('category').order_by('-published_date')
    tmp_posts_for_category = posts_for_category.values('category')
    category_lst = pd.unique(pd.DataFrame.from_records(tmp_posts_for_category)['category'])

    posts = Post.objects.exclude(title__exact='').filter(category = category, published_date__lte = timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html',{
        'posts':posts,
        'posts_for_category':category_lst,
    })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk) # 위의 4줄과 같은 역할
    comments = Comment.objects.filter(created_date__lte = timezone.now(), post=post).order_by('-created_date')
    posts_for_category = Post.objects.exclude(title__exact='').values('category').order_by('-published_date')
    tmp_posts_for_category = posts_for_category.values('category')
    category_lst = pd.unique(pd.DataFrame.from_records(tmp_posts_for_category)['category'])
    
    if request.method =="POST":
    
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            comments = Comment.objects.filter(created_date__lte = timezone.now(), post=post).order_by('-created_date')
            # return redirect('blog:post_detail', pk=post.pk)
            return render(request, 'blog/post_detail.html', {
                'posts_for_category':category_lst,
                'post':post,
                'comments':comments,
                'form':form
            })

    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {
            'posts_for_category':category_lst,
            'post':post,
            'comments':comments,
            'form':form
        })

@login_required(login_url='admin:login')
def post_new_init(request):
    post_inst = Post.objects.create(
        author = request.user
    )
    print(post_inst.pk)
    return redirect('blog:post_new', post_inst.pk)

#로그인 요구를 위한 장식자
@login_required(login_url='admin:login')
def post_new(request, pk):
    post_inst = get_object_or_404(Post, pk=pk)
    if request.method =='POST':
        form = PostForm(request.POST, request.FILES, instance=post_inst)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()

            return redirect('blog:post_detail', post.pk)
    else:
        form = PostForm(instance=post_inst)

    return render(request, 'blog/post_edit.html', {
        'form':form,
        'post':post_inst
    })

@login_required(login_url='admin:login')
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "GET":
        form  =  PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk = post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html',{
        'form':form,
        'post':post
        })

# 참고 링크: https://devofhwb.tistory.com/90
# https://cjh5414.github.io/django-file-upload/
@csrf_exempt
def fileup(request, pk):
    print(request.FILES['file'])
    # post_img_inst = Post_img.objects.create(image=request.FILES['file'], post_id=pk)
    
    url = "media" 
    return HttpResponse(url)

def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts':posts})

def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog:post_detail', pk=pk)

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
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html',{'form':form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('blog:post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('blog:post_detail',pk=comment.post.pk)

    
def about(request):
    posts_for_category = Post.objects.exclude(title__exact='').values('category').order_by('-published_date')
    tmp_posts_for_category = posts_for_category.values('category')
    category_lst = pd.unique(pd.DataFrame.from_records(tmp_posts_for_category)['category'])
    
    context={
        'posts_for_category':category_lst,
    }
    return render(request, 'blog/about.html', context)
    