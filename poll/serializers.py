from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from poll.models import Poll


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ("id", "question", "author", "published")


class PollPatchSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    question = serializers.CharField(required=False)
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    email = serializers.EmailField(allow_null=True, required=False)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError({"username": "Username must be unique"})
        return value
    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise ValidationError({"password": "Passwords must be match"})
        return super().validate(attrs)
