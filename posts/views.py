from rest_framework import status, generics
from rest_framework.views import APIView
from .models import Post, Like
from rest_framework.response import Response
from .serializers import PostSerializer, LikeSerializer
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]



class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

         # Verifica se o like já existe
        existing_like = Like.objects.filter(user=request.user, post=post)

        if existing_like.exists():
            # Se já existir o like, remove o like
            existing_like.delete()
            return Response({"detail": "Like removed."}, status=status.HTTP_200_OK)

        # Cria o like
        like = Like.objects.create(user=request.user, post=post)
        return Response(LikeSerializer(like).data, status=status.HTTP_201_CREATED)

from django.core.cache import cache

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cache_key = f"feed_{user.id}"  # Chave única para o feed de cada usuário
        cached_feed = cache.get(cache_key)

        if cached_feed is None:
            print("Cache miss")
            following_ids = user.following.values_list('followed_user', flat=True)
            posts = Post.objects.filter(user_id__in=following_ids).order_by('-created_at')[:10]
            serializer = PostSerializer(posts, many=True)
            cached_feed = serializer.data
            cache.set(cache_key, cached_feed, timeout=60*15)  # Cache por 15 minutos

        return Response(cached_feed)
