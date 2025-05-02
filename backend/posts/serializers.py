from rest_framework import serializers
from .models import Post, Like
import random, string

class PostSerializer(serializers.ModelSerializer):
    like_count = serializers.ReadOnlyField(source="post_likes.count")
    username = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    has_liked = serializers.SerializerMethodField()

    def get_has_liked(self, obj):
        request = self.context.get('request', None)
        user = request.user if request else None
        return obj.post_likes.filter(user=user).exists() if user else False

    class Meta:
        model = Post
        fields = ['id', 'text', 'image', 'created_at', 'username', 'user_id', 'like_count', 'has_liked']

    def save_renamed_image(self, instance, image):
        ext = image.name.split('.')[-1]
        rdn_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        image.name = f"post_image_{instance.id}_{rdn_str}.{ext}"
        instance.image = image
        instance.save()

    def create(self, validated_data):
        request = self.context.get('request', None)
        user = request.user if request else None
        validated_data['user'] = user
        image = validated_data.get('image', None)
        validated_data['image'] = None
        post = super().create(validated_data)
        if image:
            self.save_renamed_image(post, image)
        return post

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)

        if(instance.image and "image" in validated_data):
            instance.image.delete(False)

        image = validated_data.get('image', None)
        if image:
            self.save_renamed_image(instance, image)
        instance.save()
        return instance


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'post', 'created_at']
        read_only_fields = ['user', 'created_at']