# users/views.py
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status, generics
from django.contrib.auth.models import User
from .serializers import UserSerializer, FollowSerializer
from .models import Follow



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

class LoginView(TokenObtainPairView):
    pass

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
        print("enviando email")
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