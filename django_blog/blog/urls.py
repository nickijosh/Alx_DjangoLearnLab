from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'blog'

urlpatterns = [
    # Blog URLs
    path('', views.post_list, name='post_list'),  # example home view
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),

    # Auth URL
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
]