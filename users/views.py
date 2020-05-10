import jwt
from datetime import datetime, timedelta

from rest_framework import decorators, response, permissions, status
from rest_framework import generics

from .serializers import UserSerializer, UserCreateSerializer
from users.models import User

class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserCreateAPIView(generics.CreateAPIView):

    def create(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
