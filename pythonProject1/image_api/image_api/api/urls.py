from django.urls import path
from . import views

urlpatterns = [
    path('images/', views.ImageList.as_view(), name='image-list'),
    path('images/<int:pk>/', views.ImageDetail.as_view(), name='image-detail'),
]