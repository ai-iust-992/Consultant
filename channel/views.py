from django.shortcuts import render
import threading

from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from .serializers import *

create_link_lock = threading.Lock()


def create_uuid_link(thread_lock):
    import uuid
    with thread_lock:
        return uuid.uuid4().hex


class ChannelAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            consultant = request.user
            channel_serializer = ChannelSerializer(data=request.data)
            if channel_serializer.is_valid():
                if channel_serializer.validated_data['invite_link'] is None or not channel_serializer.validated_data[
                    'invite_link']:
                    channel_serializer.validated_data['invite_link'] = create_uuid_link(create_link_lock)
                channel_serializer.validated_data['consultant'] = consultant
                channel = channel_serializer.save()

            else:
                return Response({"error": channel_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
