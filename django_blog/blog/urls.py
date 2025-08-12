from django.urls import path, include
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    # ... your other post URLs ...
    path('accounts/', include('django.contrib.auth.urls')),  # login, logout, password reset
    path('accounts/register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.profile_view, name='profile'),
]
