from rest_framework import serializers
from channel.models import *


class ConsultantField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            "username": value.username,
            "phone_number": value.phone_number
        }


class SubscriberListField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            "username": value.username,
            "email": value.email
        }


class ChannelSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, allow_null=False,)
    consultant = ConsultantField(read_only=True, allow_null=False, allow_empty=False,)
    name = serializers.CharField(allow_null=False, allow_blank=False, required=True, max_length=50)
    description = serializers.CharField(allow_blank=True, allow_null=True, max_length=500, required=True)
    invite_link = serializers.CharField(allow_null=False, allow_blank=False, max_length=32, required=True)

    def create(self, validated_data):
        return Channel.objects.create(**validated_data)


class ChannelSubscriptionSerializer(serializers.Serializer):
    invite_link = serializers.CharField(allow_null=False, allow_blank=False, max_length=32, required=True)


