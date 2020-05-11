from django.contrib.auth import authenticate, user_logged_in
from rest_framework import serializers
from rest_framework_jwt.serializers import (
    JSONWebTokenSerializer,
    jwt_payload_handler,
    jwt_encode_handler
)

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """User seliazer."""

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'last_login')
        extra_kwargs = {"id": {"required": False}, "last_login": {"required": False}}


class UserCreateSerializer(serializers.ModelSerializer):
    """User seliazer."""

    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict):
        """Saves to User models.

        Args:
            validated_data: Contains user data.

        Retutns:
            User obj:

        """
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]
        email = validated_data["email"]
        password = validated_data["password"]

        if (email and User.objects.filter(email=email).exists()):
            raise serializers.ValidationError(
                {"email": "Email addresses must be unique."})

        user = User(first_name=first_name, last_name=last_name, email=email)
        user.set_password(password)
        user.save()
        return user


class JWTSerializer(JSONWebTokenSerializer):
    """User auth serializer."""

    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(request=self.context['request'], **credentials)

            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise serializers.ValidationError(msg)

                payload = jwt_payload_handler(user)
                user_logged_in.send(sender=user.__class__, request=self.context['request'], user=user)

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "{username_field}" and "password".'
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)
