from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from .models import Post

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        })

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({
            "token": token.key,
            "user": UserSerializer(token.user).data
        })

class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    target = get_object_or_404(User, id=user_id)
    if target == request.user:
        return Response({"detail": "You cannot follow yourself."}, status=400)
    request.user.following.add(target)  # thanks to related_name on followers
    return Response({"detail": f"Now following {target.username}."}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    target = get_object_or_404(User, id=user_id)
    if target == request.user:
        return Response({"detail": "You cannot unfollow yourself."}, status=400)
    request.user.following.remove(target)
    return Response({"detail": f"Unfollowed {target.username}."}, status=200)


class FollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            user_to_follow = CustomUser.objects.get(pk=pk)
            if request.user == user_to_follow:
                return Response({"error": "You cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST)

            request.user.following.add(user_to_follow)
            return Response({"message": f"You are now following {user_to_follow.username}"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            user_to_unfollow = CustomUser.objects.get(pk=pk)
            if request.user == user_to_unfollow:
                return Response({"error": "You cannot unfollow yourself"}, status=status.HTTP_400_BAD_REQUEST)

            request.user.following.remove(user_to_unfollow)
            return Response({"message": f"You have unfollowed {user_to_unfollow.username}"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@login_required
def user_list(request):
    users = CustomUser.objects.all().exclude(id=request.user.id)
    return render(request, 'accounts/user_list.html', {'users': users})

@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(CustomUser, id=user_id)
    request.user.following.add(user_to_follow)
    return redirect('user_list')

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
    request.user.following.remove(user_to_unfollow)
    return redirect('user_list')

@login_required
def feed_view(request):
    # get the users the current user follows
    following_users = request.user.profile.following.all()  # adjust if your follow model differs

    # filter posts from those users and order by creation date (descending)
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

    return render(request, "posts/feed.html", {"posts": posts})

