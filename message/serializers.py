from rest_framework import serializers
from message.models import *


class ChannelMessageCreatorField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            "id": value.id,
            "username": value.username,
            "phone_number": value.phone_number
        }


class ChannelMessageSerializer(serializers.Serializer):
    message_id = serializers.IntegerField(read_only=True)
    channel_id = serializers.IntegerField(required=True, allow_null=False)
    creator = ChannelMessageCreatorField(allow_null=False, allow_empty=False, read_only=True)
    text = serializers.CharField(max_length=2000)
    message_choice = [
        ('t', 'text'),
        ('i', 'image'),
        ('v', 'video'),
        ('a', 'audio'),
    ]
    message_type = serializers.ChoiceField(choices=message_choice, required=True, allow_null=False,
                                           allow_blank=False)
    message_file = serializers.FileField(required=False, allow_null=False, allow_empty_file=False)

    def create(self, validated_data):
        del validated_data['channel_id']
        return ChannelMessage.objects.create(**validated_data)
