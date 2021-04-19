from abc import ABC

from rest_framework import serializers
from .models import *


class RequestTargetUser(serializers.RelatedField):
    def to_representation(self, value):
        return {
            "username": value.username,
            "email": value.email
        }


class UserSignupSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_null=False, allow_blank=False, max_length=128)
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)
    first_name = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    last_name = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    phone_number = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    password = serializers.CharField(required=True, allow_null=False, allow_blank=False, min_length=6, max_length=25)
    password_repetition = serializers.CharField(required=True, allow_null=False, allow_blank=False, min_length=6,
                                                max_length=25)
    private_profile = serializers.BooleanField(default=False, allow_null=False)

    def create(self, validated_data):
        del validated_data['password_repetition']
        return UserProfile.objects.create(**validated_data)

    def validate_password(self, password):
        """
        Check the password regex.
        """
        # TODO WRITE PASSWORD VALIDATION
        return password

    def validate(self, data):
        """
        Check the password regex.
        """
        if data["password_repetition"] != data["password"]:
            raise serializers.ValidationError("Repetition of password is not same with password!")
        return data

    def validate_phone_number(self, phone_number):
        """
        Check the phone_number regex.
        """
        import re
        if len(phone_number) != 11 or re.search(r"09[0-9]{9}", phone_number) is None:
            raise serializers.ValidationError("Format of phone_number is not true")
        return phone_number


class UserConsultantLoginSerializer(serializers.Serializer):
    auth = serializers.CharField(required=False)
    email_username = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    password = serializers.CharField(required=True, allow_null=False, allow_blank=False, min_length=6)


class UserConsultantSerializerReturnData(serializers.Serializer):
    user_or_consultant_choice = (
        ('User', 'User'),
        ('Consultant', 'Consultant')
    )
    # auth = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    auth = serializers.CharField(required=False)
    username = serializers.CharField(required=True, allow_null=False, allow_blank=False, max_length=128)
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)
    first_name = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    last_name = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    phone_number = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    private_profile = serializers.BooleanField(default=False, allow_null=False)
    user_or_consultant = serializers.ChoiceField(required=False, choices=user_or_consultant_choice)


class ConsultanSignupSerializer(UserSignupSerializer):
    consultant_types = (
        ('Lawyer', 'Lawyer'),
        ('medical', 'medical'),
        ('Entrance_Exam', 'Entrance_Exam'),
        ('Psychology', 'Psychology'),
        ('Educationalـimmigration', 'Educationalـimmigration'),
        ('Academicـadvice', 'Academicـadvice')
    )
    user_type = serializers.ChoiceField(choices=consultant_types, required=True)
    certificate = serializers.FileField(required=True, allow_null=False, allow_empty_file=False)

    def create(self, validated_data):
        del validated_data['password_repetition']
        return ConsultantProfile.objects.create(**validated_data)

    def validate_certificate(self, certificate_file):
        # TODO CHECK CERTIFICATE EXTENSION
        return certificate_file


class RequestSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, allow_null=False)
    target_user = serializers.CharField(required=True, allow_null=False, allow_blank=False, )
    request_text = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=2000)
    request_type_choices = [
        ('join_channel', 'join_channel'),
        ('secretary', 'secretary'),
    ]
    request_type = serializers.ChoiceField(required=True, choices=request_type_choices)

    def create(self, validated_data):
        return Request.objects.create(**validated_data)


class AnswerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, allow_null=False)
    target_user = RequestTargetUser(read_only=True, allow_null=False, allow_empty=False)
    request_text = serializers.CharField(read_only=True, allow_null=True, allow_blank=True, max_length=2000)
    answer_text = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=2000)
    request_date = serializers.DateTimeField(read_only=True, allow_null=False, )
    answer_date = serializers.DateTimeField(allow_null=True, required=False)
    accept = serializers.BooleanField(required=True, allow_null=False)
    request_type_choices = [
        ('join_channel', 'join_channel'),
        ('secretary', 'secretary'),
    ]
    request_type = serializers.ChoiceField(allow_null=False, allow_blank=False, choices=request_type_choices)
