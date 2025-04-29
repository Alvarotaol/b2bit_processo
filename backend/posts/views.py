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


    #Impede que usuários apaguem posts de outros usuários
    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        if post.user == request.user:
            return self.destroy(request, *args, **kwargs)
        else:
            return Response({"detail": "You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)



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
            following_ids = user.following.values_list('followed_user', flat=True)
            following_ids = list(following_ids)
            following_ids.append(user.id)
            posts = Post.objects.filter(user_id__in=following_ids).order_by('-created_at')[:10]
            serializer = PostSerializer(posts, many=True, context={'request': request})
            cached_feed = serializer.data
            cache.set(cache_key, cached_feed, timeout=60*15)  # Cache por 15 minutos

        paginated_feed = self.paginator.paginate_queryset(cached_feed, request)
        return self.paginator.get_paginated_response(paginated_feed)


class PostSearchView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Post.objects.all()
        query = self.request.query_params.get('q')
        if query:
            queryset = queryset.filter(text__icontains=query)
        return queryset