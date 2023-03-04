from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    image_file = models.ImageField(upload_to='images/')
    thumbnail_200 = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    thumbnail_400 = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    original_image_url = models.URLField(null=True, blank=True)
    expiring_image_url = models.URLField(null=True, blank=True)