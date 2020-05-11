from django.urls import path, include

from .views import UserListAPIView, UserCreateAPIView
from rest_framework_jwt.views import ObtainJSONWebToken

urlpatterns = [
    path('', UserListAPIView.as_view()),
    path('login/', ObtainJSONWebToken.as_view()),
    path('register/', UserCreateAPIView.as_view()),
]
