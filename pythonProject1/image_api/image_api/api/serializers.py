from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Image

class ImageSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.ReadOnlyField()
    original_url = serializers.ReadOnlyField()
    expiring_url = serializers.ReadOnlyField()

    class Meta:
        model = Image
        fields = ('id', 'user', 'image', 'thumbnail_url', 'original_url', 'expiring_url')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')