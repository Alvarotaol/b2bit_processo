from rest_framework import serializers
from .models import Post, Like

class PostSerializer(serializers.ModelSerializer):
    like_count = serializers.ReadOnlyField(source="post_likes.count")
    user = serializers.ReadOnlyField(source='user.id')
    bla = serializers.ReadOnlyField(source='get_bla')

    class Meta:
        model = Post
        fields = ['id', 'text', 'image', 'created_at', 'user', 'like_count', 'bla']
        read_only_fields = ['id', 'created_at', 'user', 'like_count', 'bla']

    #def get_like_count(self, obj):
    #    print(obj.post_likes.count())
    #    return obj.post_likes.count()

    #def get_bla(self, obj):
    #    return "bla"

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'post', 'created_at']
        read_only_fields = ['user', 'created_at']