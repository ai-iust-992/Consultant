from rest_framework import serializers
from .models import *


class RequestTargetUser(serializers.RelatedField):
    def to_representation(self, value):
        return {
            "username": value.username,
            "email": value.email
        }


class RequestSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, allow_null=False)
    target_user = serializers.CharField(required=True, allow_null=False, allow_blank=False, )
    request_text = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=2000)
    request_type_choices = [
        ('join_channel', 'join_channel'),
        ('secretary', 'secretary'),
    ]
    request_type = serializers.ChoiceField(choices=request_type_choices, read_only=True)

    def create(self, validated_data):
        return Request.objects.create(**validated_data)


class AnswerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, allow_null=False)
    target_user = RequestTargetUser(read_only=True, allow_null=False, allow_empty=False)
    request_text = serializers.CharField(read_only=True, allow_null=True, allow_blank=True, max_length=2000)
    answer_text = serializers.CharField(required=False, allow_null=True, allow_blank=True, max_length=2000)
    request_date = serializers.DateTimeField(read_only=True, allow_null=False, )
    answer_date = serializers.DateTimeField(read_only=True, allow_null=True, )
    accept = serializers.BooleanField(required=True, allow_null=False)
    request_type_choices = [
        ('join_channel', 'join_channel'),
        ('secretary', 'secretary'),
    ]
    request_type = serializers.ChoiceField(allow_null=False, allow_blank=False, choices=request_type_choices,
                                           read_only=True)

    def update(self, request_instance, validated_data):
        request_instance.answer_text = validated_data.get('answer_text', request_instance.answer_text)
        request_instance.accept = validated_data.get('accept', request_instance.accept)
        request_instance.answer_date = timezone.now()
        request_instance.save()
        return request_instance
