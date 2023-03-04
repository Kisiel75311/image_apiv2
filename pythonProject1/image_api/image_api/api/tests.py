from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Image
from .serializers import ImageSerializer, UserSerializer

class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_serializer_returns_correct_data(self):
        serializer = UserSerializer(instance=self.user)
        expected_data = {'id': self.user.id, 'username': self.user.username, 'email': self.user.email}
        self.assertEqual(serializer.data, expected_data)


class ImageSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.image = Image.objects.create(user=self.user, image='test_image.jpg', thumbnail_200='test_thumbnail_200.jpg',
                                           thumbnail_400='test_thumbnail_400.jpg', original_image_url='test_original_image_url.jpg',
                                           expiring_image_url='test_expiring_image_url.jpg')

    def test_serializer_returns_correct_data(self):
        serializer = ImageSerializer(instance=self.image)
        expected_data = {'id': self.image.id, 'user': self.user.id, 'image': self.image.image, 'thumbnail_url': self.image.thumbnail_url,
                         'original_url': self.image.original_url, 'expiring_url': self.image.expiring_url}
        self.assertEqual(serializer.data, expected_data)


class ImageListCreateAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('image_list_create')

    def test_get_image_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_image(self):
        data = {'image': 'test_image.jpg'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ImageDetailAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.image = Image.objects.create(user=self.user, image='test_image.jpg', thumbnail_200='test_thumbnail_200.jpg',
                                           thumbnail_400='test_thumbnail_400.jpg', original_image_url='test_original_image_url.jpg',
                                           expiring_image_url='test_expiring_image_url.jpg')
        self.url = reverse('image_detail', args=[self.image.id])

    def test_get_image_detail(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_image(self):
        data = {'image': 'updated_image.jpg'}
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_image(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class ThumbnailAPIViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.image = Image.objects.create(
            user=self.user,
            image=SimpleUploadedFile(
                name='test_image.jpg',
                content=BytesIO(b'example content'),
                content_type='image/jpeg'
            )
        )

    def test_thumbnail_200(self):
        url = reverse('thumbnail', args=[self.image.id, 200])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type'), 'image/jpeg')
        self.assertEqual(response.get('Content-Length'), '9626')

    def test_thumbnail_400(self):
        url = reverse('thumbnail', args=[self.image.id, 400])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type'), 'image/jpeg')
        self.assertEqual(response.get('Content-Length'), '30708')

    def test_invalid_size(self):
        url = reverse('thumbnail', args=[self.image.id, 500])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
