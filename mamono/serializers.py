from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    username = serializers.CharField()
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email']