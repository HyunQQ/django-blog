from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from blog import views

app_name='blog'

urlpatterns=[
    path('', views.post_list, name='post_list'),
    path('<str:category>', views.post_category_list, name='post_category_list'),
    path('post/detail_<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new_init/', views.post_new_init, name='post_new_init'),
    path('post/new/<int:pk>', views.post_new, name='post_new'),
    path('post/<int:pk>/edit', views.post_edit, name='post_edit'),
    path('fileup/<int:pk>', views.fileup, name="fileup"),
    path('draft/', views.post_draft_list, name ='post_draft_list'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<int:pk>/remove/', views.post_remove, name='post_remove'),
    # path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    # path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    # path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('about/', views.about, name='about'),
    path('signin/', views.signin, name='signin'),
]

# 미디어 파일 세팅
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)