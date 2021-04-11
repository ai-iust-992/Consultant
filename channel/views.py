from django.shortcuts import render
import threading

from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from rest_framework.views import APIView

from .serializers import *

create_link_lock = threading.Lock()


def create_uuid_link(thread_lock):
    import uuid
    with thread_lock:
        return uuid.uuid4().hex


class CreateLinkAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            unique_link = create_uuid_link(create_link_lock)
            return Response(data={
                "invite_link": unique_link,
            }, status=status.HTTP_200_OK)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChannelAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            consultant = ConsultantProfile.objects.filter(baseuser_ptr_id=request.user.id)
            if len(consultant) == 0:
                return Response("You do not have permission to perform this action", status=status.HTTP_403_FORBIDDEN)
            consultant = consultant[0]
            channel_serializer = ChannelSerializer(data=request.data)
            if channel_serializer.is_valid():
                channel_serializer.validated_data['consultant'] = consultant
                channel = channel_serializer.save()
                channel_serializer = ChannelSerializer(channel)
                return Response(
                    data=channel_serializer.data,
                    status=status.HTTP_200_OK
                )
            else:
                return Response({"error": channel_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChannelSubscriptionAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            user = UserProfile.objects.filter(baseuser_ptr_id=request.user.id)
            if len(user) == 0:
                user = ConsultantProfile.objects.filter(baseuser_ptr_id=request.user.id)

            user = user[0]
            subscription_serializer = ChannelSubscriptionSerializer(data=request.data)
            if subscription_serializer.is_valid():
                channel = Channel.objects.filter(invite_link=subscription_serializer.validated_data['invite_link'])
                if len(channel) == 0:
                    return Response({"error": "Channel with this invite-link is not exists"},
                                    status=status.HTTP_400_BAD_REQUEST)
                # TODO CHECK CHANNEL secretaries
                if channel[0].consultant.baseuser_ptr_id == request.user.id:
                    return Response({"error": "You are consultant of this channel!!!"},
                                    status=status.HTTP_400_BAD_REQUEST)
                subscriber = Subscription(user=user, channel=channel[0])
                subscriber.save()
                return Response(
                    data="ok",
                    status=status.HTTP_200_OK
                )
            else:
                return Response({"error": subscription_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SearchChannel(APIView):
    permission_classes = []
    def get(self, request, format=None):
        try:
            from django.db.models import Q
            query = request.GET['query'] # string
            
            if request.GET.get('search_category') != None:
                search_caregory = request.GET['search_category']
            data = []
            if request.GET.get('search_category') != None:
              #  ch = Channel.objects.filter(consultant==)
                Channels = Channel.objects.filter(consultant__user_type__in=search_caregory).filter(Q(name__icontains=query))
                for channel in Channels:
                    data.append({
                        'name': channel.name,
                        'description': channel.description,
                        'invite_link': channel.invite_link,
                    })
                Channels = Channel.objects.filter(consultant__user_type__in=search_caregory).filter(Q(description__icontains=query))            
                for channel in Channels:
                    data.append({
                        'name': channel.name,
                        'description': channel.description,
                        'invite_link': channel.invite_link,
                    })
            else:
                Channels = Channel.objects.filter(Q(name__icontains=query))
                for channel in Channels:
                    data.append({
                        'name': channel.name,
                        'description': channel.description,
                        'invite_link': channel.invite_link,
                    })
                Channels = Channel.objects.filter(Q(description__icontains=query))            
                for channel in Channels:
                    data.append({
                        'name': channel.name,
                        'description': channel.description,
                        'invite_link': channel.invite_link,
                    })

            return Response({'data': data}, status=status.HTTP_200_OK)
        except: 
            return Response({'status': "Internal Server Error, We'll Check it later!"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)    