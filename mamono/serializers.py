from rest_framework import serializers
from django.contrib.auth.models import User

from mamono.models import DiscordUser


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    username = serializers.CharField()
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class DiscordUserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    user = serializers.CharField()
    is_active = serializers.BooleanField()

    class Meta:
        model = DiscordUser
        fields = ['id', 'user', 'is_active']

class DiscordGuildSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    guild = serializers.CharField()
    owner = serializers.CharField()
    name = serializers.CharField()
    is_active = serializers.BooleanField()

    class Meta:
        fields = ['id', 'guild', 'owner', 'name', 'is_active']

class LevelSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    guild = DiscordGuildSerializer()
    user = DiscordUserSerializer()
    level = serializers.IntegerField()
    experience = serializers.IntegerField()

    class Meta:
        fields = ['id', 'guild', 'user', 'level', 'experience']