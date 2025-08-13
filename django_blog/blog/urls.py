from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    PostListView, PostDetailView, PostCreateView,
    PostUpdateView, PostDeleteView, CommentCreateView, CommentUpdateView, CommentDeleteView  # ✅ Added
)

app_name = 'blog'

urlpatterns = [
    # Blog URLs
    path('', views.post_list, name='post_list'),  # example home view
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    # ✅ Added missing update path for the check
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),

    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),

    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/new/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    # Auth URL
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    # Comment URLs
    path('posts/<int:post_id>/comments/new/', views.add_comment, name='add_comment'),
    path('comments/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),

    path('post/<int:pk>/comment/new/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment-create'),

]
