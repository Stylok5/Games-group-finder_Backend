from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    def validate(self, data):
        password = data.pop('password', None)
        password_confirmation = data.pop('password_confirmation', None)

        if password and password_confirmation:
            if password != password_confirmation:
                raise serializers.ValidationError("Passwords do not match")
            password_validation.validate_password(password)
            data['password'] = make_password(password)
        return data

    class Meta:
        model = User
        fields = 'id', 'email', 'description', 'profile_image', 'username', 'password', 'password_confirmation', 'date_joined'
