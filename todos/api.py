from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ["email", "username", "password", "password2"]
        extra_kwargs = {
            'password': {'write_only': True},
        }
    def save(self):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class TeamSerializer(serializers.ModelSerializer):
    class Meta :
        model = Team
        fields = "__all__"


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta :
        model = AdminUser
        fields = "__all__"


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = "__all__"


class AskToBeAdminSerializer(serializers.ModelSerializer):
    class Meta :
        model = AskToBeAdmin
        fields = "__all__"
