from django.shortcuts import render
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from rest_framework.views import APIView

from User.models import ConsultantProfile
from .serializers import *


class ChannelMessageAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            message_serializer = ChannelMessageSerializer(data=request.data)
            if message_serializer.is_valid():
                channel = Channel.objects.filter(id=message_serializer.validated_data['channel_id']).select_related(
                    'consultant')
                if len(channel) == 0:
                    return Response({"error": "channel_id is not exists"}, status=status.HTTP_400_BAD_REQUEST)
                message_creator = request.user
                if channel[0].consultant.baseuser_ptr_id != request.user.id and len(
                        ConsultantProfile.my_secretaries.through.objects.filter(
                                consultantprofile_id=channel[0].consultant.id, userprofile_id=request.user.id)) == 0:
                    return Response({"error": "You dont have permission for this request"}, status=status.HTTP_403_FORBIDDEN)
                message_serializer.validated_data['creator'] = message_creator
                message_serializer.validated_data['channel'] = channel[0]
                message = message_serializer.save()
                message_serializer = ChannelMessageSerializer(message)
                return Response(message_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": message_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
