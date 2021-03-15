from abc import ABC

from rest_framework import serializers
from .models import *


class UserSignupSerializer(serializers.Serializer, ABC):
    username = serializers.CharField(required=True, allow_null=False, allow_blank=False, max_length=128)
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)
    first_name = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    last_name = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    phone_number = serializers.CharField(required=True, allow_blank=False, allow_null=False, max_length=11)
    password = serializers.CharField(required=True, allow_null=False, allow_blank=False, min_length=6, max_length=25)
    password_repetition = serializers.CharField(required=True, allow_null=False, allow_blank=False, min_length=6,
                                                max_length=25)
    is_private = serializers.BooleanField(default=False, allow_null=False)

    def create(self, validated_data):
        return UserProfile.objects.create(**validated_data)

    def validate_password(self, password):
        """
        Check the password regex.
        """
        # TODO WRITE PASSWORD VALIDATION
        return password

    def validate_password_repetition(self, password_repetition):
        """
        Check the password regex.
        """
        # TODO WRITE PASSWORD_REPETITION VALIDATION
        return password_repetition

    def validate_phone_number(self, phone_number):
        """
        Check the phone_number regex.
        """
        # TODO WRITE PHONE_NUMBER VALIDATION
        return phone_number


class LawyerSignupSerializer(UserSignupSerializer, ABC):
    certificate = serializers.FileField(required=True, allow_null=False, allow_empty_file=False)

    def create(self, validated_data):
        return Lawyer.objects.create(**validated_data)

    def validate_certificate(self, certificate_file):
        # TODO CHECK CERTIFICATE EXTENSION
        pass
