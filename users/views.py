"""User views."""

from datetime import datetime, timedelta

from rest_framework import decorators, response, permissions, status
from rest_framework import generics
from rest_framework_jwt.views import ObtainJSONWebToken

from .serializers import UserSerializer, UserCreateSerializer, JWTSerializer
from users.models import User


class UserListAPIView(generics.ListAPIView):
    """User list view."""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """User create view."""

    def create(self, request):
        """Creates new user into database.

        Args:
            request (Request obj): Contains all needed information about user.

        Returns:
            (Response obj): Sends response for user about user or error.

        """
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginApiView(ObtainJSONWebToken):
    """User login view."""

    serializer_class = JWTSerializer
