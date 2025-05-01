# users/views.py
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status, generics
from django.contrib.auth import logout, get_user_model
from .serializers import UserSerializer, FollowSerializer
from .models import Follow
from posts.models import Post
User = get_user_model()


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'followers_count': user.followers.count(),
            'following_count': user.following.count()
        })

class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'signup'

class LoginView(TokenObtainPairView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'login'

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)

class TokenRefreshView(TokenRefreshView):
    pass

from .tasks import send_new_follower_email
class FollowUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        # Tenta seguir o usuário
        try:
            followed_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Verifica se o usuário já segue o outro
        if Follow.objects.filter(user=request.user, followed_user=followed_user).exists():
            return Response({'detail': 'You are already following this user.'}, status=status.HTTP_400_BAD_REQUEST)

        # Cria o relacionamento de seguimento
        follow = Follow.objects.create(user=request.user, followed_user=followed_user)

        # Envia email de notificação para o outro usuário
        send_new_follower_email.delay(followed_user.email, request.user.username)
        return Response(FollowSerializer(follow).data, status=status.HTTP_201_CREATED)

class UnfollowUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        # Tenta deixar de seguir o usuário
        try:
            followed_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Verifica se o usuário está seguindo o outro
        follow = Follow.objects.filter(user=request.user, followed_user=followed_user).first()
        if not follow:
            return Response({'detail': 'You are not following this user.'}, status=status.HTTP_400_BAD_REQUEST)

        # Deleta o relacionamento de seguimento
        follow.delete()
        return Response({'detail': 'Successfully unfollowed.'}, status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id=None):
        user = request.user if user_id is None else User.objects.filter(id=user_id).first()
        if not user:
            return Response({"detail": "User not found."}, status=404)

        is_own_profile = user == request.user
        is_following = None if is_own_profile else request.user.following.filter(followed_user=user.id).exists()

        return Response({
            "id": user.id,
            "username": user.username,
            "followers_count": user.followers.count(),
            "following_count": user.following.count(),
            "is_following": is_following,
        })

from posts.serializers import PostSerializer

class UserPostsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = [PostSerializer]

    def get(self, request, user_id):
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response({"detail": "Usuário não encontrado"}, status=404)

        posts = Post.objects.filter(user=user).order_by("-created_at")
        posts_data = PostSerializer(posts, many=True).data
        paginate_posts = self.paginator.paginate_queryset(posts_data, request)
        return self.paginator.get_paginated_response(paginate_posts)


from .serializers import UserSuggestionSerializer

class UserSuggestionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        following_ids = user.following.values_list("followed_user", flat=True)
        suggestions = User.objects.exclude(id__in=following_ids).exclude(id=user.id)[:10]

        serializer = UserSuggestionSerializer(suggestions, many=True)
        return Response(serializer.data)
