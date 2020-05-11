"""Users URL Configuration."""

from django.urls import path

from .views import UserListAPIView, UserCreateAPIView, UserLoginApiView
from rest_framework_jwt.views import ObtainJSONWebToken

urlpatterns = [
    path('', UserListAPIView.as_view()),
    path('login/', UserLoginApiView.as_view()),
    path('register/', UserCreateAPIView.as_view()),
]
