from rest_framework import serializers
from .models import Image

class ImageSerializer(serializers.ModelSerializer):
    thumbnail_200 = serializers.ImageField(read_only=True)
    thumbnail_400 = serializers.ImageField(read_only=True)
    image_url = serializers.URLField(read_only=True)
    expiring_image_url = serializers.URLField(read_only=True)

    class Meta:
        model = Image
        fields = ('id', 'user', 'name', 'image', 'thumbnail_200', 'thumbnail_400', 'image_url', 'expiring_image_url')