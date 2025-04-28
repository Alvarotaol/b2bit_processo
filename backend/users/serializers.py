# users/serializers.py

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Follow

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['user', 'followed_user', 'created_at']
        read_only_fields = ['user', 'created_at']

    def validate(self, data):
        """
        Valida se o usuário não está tentando seguir a si mesmo.
        """
        if data['user'] == data['followed_user']:
            raise serializers.ValidationError("You cannot follow yourself.")
        return data
