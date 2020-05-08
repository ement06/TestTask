from rest_framework import serializers
# from rest_framework_simplejwt.serializers import TokenObtainSerializer

from users.models import User


class UserLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        models = User
        fields = ["email", "password"]
        extra_kwargs = {"password": {"write_only": True}}
            
            


class UserCreateSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
        ]
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
