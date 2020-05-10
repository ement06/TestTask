from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'last_login')
        extra_kwargs = {"id": {"required": False}, "last_login": {"required": False}}

class UserCreateSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}


    def create(self, validated_data):
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
