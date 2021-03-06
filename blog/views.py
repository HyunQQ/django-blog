import pandas as pd
import os

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.views.generic import View
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Min
from django.conf import settings

from .models import Post, Post_img
from .forms import PostForm, LoginForm
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

    if Post.objects.exclude(title__exact='').values('category').exists():
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
    else:
        return render(request, 'blog/post_list.html')

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
    post = get_object_or_404(Post, pk=pk) # 404 error 처리
    posts_for_category = Post.objects.exclude(title__exact='').values('category').order_by('-published_date')
    tmp_posts_for_category = posts_for_category.values('category')
    category_lst = pd.unique(pd.DataFrame.from_records(tmp_posts_for_category)['category'])
    context = {
        'posts_for_category':category_lst,
        'post':post,
        'pk':str(pk),
    }
    context['post_absolute_url'] = request.build_absolute_uri(reverse('blog:post_detail', args=(pk,)))

    return render(request, 'blog/post_detail.html', context)

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
# 파일 업로드 및 파일 url 전달
def fileup(request, pk):
    post_img_inst = Post_img.objects.create(image=request.FILES['file'], post_id=pk)
    img_url = str(post_img_inst.image)
    return HttpResponse(img_url)

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


    
def about(request):
    posts_for_category = Post.objects.exclude(title__exact='').values('category').order_by('-published_date')
    tmp_posts_for_category = posts_for_category.values('category')
    category_lst = pd.unique(pd.DataFrame.from_records(tmp_posts_for_category)['category'])
    
    context={
        'posts_for_category':category_lst,
    }
    return render(request, 'blog/about.html', context)

def signin(request):
    if request.method =="POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password=password)
        if user is not None:
            login(request, user)
            return redirect('blog:post_list')
        else:
            err_message="아이디나 비밀번호가 일치하지 않습니다. 확인해주시기바랍니다."
            context = {
                'err_message':err_message,
                'form':form
            }
            return render(request, 'registration/login.html', context)

        
    else:
        form = LoginForm()
        return render(request, 'registration/login.html', {'form':form})

    ##############기존 comment ####################
    # def add_comment_to_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form  = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.save()
#             return redirect('blog:post_detail', pk=post.pk)
#     else:
#         form = CommentForm()
#     return render(request, 'blog/add_comment_to_post.html',{'form':form})

# @login_required
# def comment_approve(request, pk):
#     comment = get_object_or_404(Comment,pk=pk)
#     comment.approve()
#     return redirect('blog:post_detail', pk=comment.post.pk)

# @login_required
# def comment_remove(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     comment.delete()
#     return redirect('blog:post_detail',pk=comment.post.pk)
