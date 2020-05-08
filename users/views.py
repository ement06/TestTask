import jwt

from datetime import datetime, timedelta

from django.contrib.auth import logout
from rest_framework import decorators, response, permissions, status

from .serializers import UserCreateSerializer, UserLoginSerializer
from users.models import User

def check_exist(data):
    email = data['email']
    password = data['password']
    user = User.objects.filter(email=email).first()
    if user and user.check_password(password):
        return user


@decorators.api_view(['POST'])
@decorators.permission_classes([permissions.AllowAny])
def login_view(request):
    serializer = UserLoginSerializer(data=request.data)

    if check_exist(request.data):
        token = jwt.encode({
            'email': request.data['email'],
            'exp': datetime.utcnow() + timedelta(hours=6)
        }, 'secret')
        return response.Response(token, status.HTTP_201_CREATED)


@decorators.api_view(['POST'])
@decorators.permission_classes([permissions.AllowAny])
def registration_view(request):
    serializer = UserCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    user = serializer.save()
    token = jwt.encode({
        'email': request.data['email'],
        'exp': datetime.utcnow() + timedelta(hours=6)
    }, 'secret')
    return response.Response(token, status.HTTP_201_CREATED)

@decorators.api_view(['POST'])
# @decorators.permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    print(request)
    logout(request)
    return response.Response('You are succsesfuly logout', status.HTTP_200_OK)