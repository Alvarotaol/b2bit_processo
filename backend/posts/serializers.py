from rest_framework import serializers
from .models import Post, Like

class PostSerializer(serializers.ModelSerializer):
    like_count = serializers.ReadOnlyField(source="post_likes.count")
    user = serializers.ReadOnlyField(source='user.username')
    has_liked = serializers.SerializerMethodField()

    def get_has_liked(self, obj):
        request = self.context.get('request', None)
        user = request.user if request else None
        return obj.post_likes.filter(user=user).exists() if user else False

    class Meta:
        model = Post
        fields = ['id', 'text', 'image', 'created_at', 'user', 'like_count', 'has_liked']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'post', 'created_at']
        read_only_fields = ['user', 'created_at']