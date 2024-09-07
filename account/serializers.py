from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from account.models import Account, Interest, AccountProfile


class AccountSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    # email = serializers.EmailField(required=True, allow_null=False)
    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password2"):
            raise serializers.ValidationError("Passwords must be match")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        account: Account = super().create(validated_data)
        account.set_password(validated_data["password"])
        account.save()
        return account

    class Meta:
        model = Account
        fields = ("id", "username", "email", "password", "password2", "first_name", "last_name", "phone")
        extra_kwargs = {
            'email': {'required': True, 'allow_null': False},
            'first_name': {'required': True, 'allow_null': False},
            'last_name': {'required': True, 'allow_null': False}
        }


class AccountProfileSerializer(ModelSerializer):
    passport_number = serializers.CharField(required=False)
    passport_letter = serializers.CharField(required=False)
    class Meta:
        model = AccountProfile
        fields = ('city', 'passport_number', 'passport_letter')
        # extra_kwargs = {
        #     'city': {'required': False, 'allow_null': True},
        #     'passport_number': {'required': False, 'allow_null': True},
        #     'passport_letter': {'required': False, 'allow_null': True},
        # }

class AccountDetialSeriaizer(ModelSerializer):
    profile = AccountProfileSerializer()

    class Meta:
        model = Account
        fields = ("id", "username", "email", "first_name", "last_name", "phone", "profile")
        extra_kwargs = {
            'email': {'required': False, 'allow_null': True},
            'first_name': {'required': False, 'allow_null': True},
            'last_name': {'required': False, 'allow_null': True},
            'profile': {'required': False, 'allow_null': True}
        }

    # def update(self, instance, validated_data):
    #     return super().update(instance, validated_data)

    def update(self, instance, validated_data):
        profile = validated_data.pop("profile")
        super().update(instance, validated_data)
        account_profile = instance.profile
        for key, value in profile.items():
            setattr(account_profile, key, value)
        account_profile.save()
        return instance


class InterestSerializer(ModelSerializer):
    class Meta:
        model = Interest
        fields = ("name", "slug")
        extra_kwargs = {
            'slug': {'required': False, 'allow_null': True, "read_only": True},
        }
