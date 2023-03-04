from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Image
from .serializers import UserSerializer, ImageSerializer

class ImageList(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ImageListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ImageDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)


class ThumbnailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, size):
        image = get_object_or_404(Image, pk=pk, user=request.user)
        if size == '200':
            thumbnail = image.thumbnail_200
        elif size == '400':
            thumbnail = image.thumbnail_400
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if not thumbnail:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(thumbnail.url)


class OriginalImageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        image = get_object_or_404(Image, pk=pk, user=request.user)
        if not image.original_image_url:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(image.original_image_url)


class ExpiringImageURLAPIView(APIView):
    pass
    # permission_classes = [IsAuthenticated]
    #
    #
    # def post(self, request, pk):
    #     image = get_object_or_404(Image, pk=pk, user=request.user)
    #     seconds = request.data.get('seconds')
    #     if not 300 <= seconds <= 30000:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #     # expiring_image_url = ...
    #     image.expiring_image_url = expiring_image_url
    #     image.save()
    #     return Response(expiring_image_url)
