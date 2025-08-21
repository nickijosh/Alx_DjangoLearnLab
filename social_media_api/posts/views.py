from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework import filters

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "content"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        followed_users = self.request.user.following.all()
        return Post.objects.filter(author__in=followed_users).order_by('-created_at')
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_feed(request):
    # Get the users the current user is following
    following_users = request.user.following.all()
    
    # Get posts from those users, ordered by most recent first
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
