from django.shortcuts import render
import threading

from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.views import APIView

from User.models import UserProfile
from .serializers import *
from .models import *

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

    def get(self, request, channelId, format=None):
        try:
            channel = Channel.objects.filter(id=channelId).select_related('consultant')
            if len(channel) == 0:
                return Response({"error": "This channel id is not exits"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(ChannelSerializer(channel[0]).data, status=status.HTTP_200_OK)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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


class UserChannelsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            user_is_subscriber = Channel.objects.filter(subscribers=request.user)
            user_is_consultant = Channel.objects.filter(consultant=request.user)
            user_is_secretary = Channel.objects.filter(consultant__my_secretaries=request.user)
            user_channels = []
            for channel in user_is_consultant:
                user_channels += [
                    {
                        "id": channel.id,
                        "name": channel.name,
                        "description": channel.description,
                        "invite_link": channel.invite_link,
                        "user_role": "consultant"
                    }
                ]
            for channel in user_is_secretary:
                user_channels += [
                    {
                        "id": channel.id,
                        "name": channel.name,
                        "description": channel.description,
                        "invite_link": channel.invite_link,
                        "user_role": "secretary"
                    }
                ]
            for channel in user_is_subscriber:
                user_channels += [
                    {
                        "id": channel.id,
                        "name": channel.name,
                        "description": channel.description,
                        "invite_link": channel.invite_link,
                        "user_role": "subscriber"
                    }
                ]
            return Response(user_channels, status=status.HTTP_200_OK)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserRoleInChannelAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, channelId, format=None):
        try:
            channel = Channel.objects.filter(id=channelId).select_related('consultant__my_secretaries')
            if len(channel) == 0:
                return Response({"error": "This channel id is not exits"}, status=status.HTTP_400_BAD_REQUEST)
            if channel[0].consultant.id == request.user.id:
                return Response(data={"role": "consultant", "invite_link": channel[0].invite_link},
                                status=status.HTTP_200_OK)
            for secretary in channel[0].consultant.my_secretaries.all():
                if request.user.id == secretary.id:
                    return Response(data={"role": "secretary", "invite_link": channel[0].invite_link},
                                    status=status.HTTP_200_OK)
            for subscriber in channel[0].subscribers.all():
                if request.user.id == subscriber.id:
                    return Response(data={"role": "subscriber", "invite_link": channel[0].invite_link},
                                    status=status.HTTP_200_OK)
            return Response(data={"role": "nothing", "invite_link": channel[0].invite_link},
                            status=status.HTTP_200_OK)
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
                channel = Channel.objects.filter(
                    invite_link=subscription_serializer.validated_data['invite_link']).select_related('consultant')
                if len(channel) == 0:
                    return Response({"error": "Channel with this invite-link is not exists"},
                                    status=status.HTTP_400_BAD_REQUEST)
                if channel[0].consultant.baseuser_ptr_id == request.user.id:
                    return Response({"error": "You are consultant of this channel!!!"},
                                    status=status.HTTP_400_BAD_REQUEST)
                if len(ConsultantProfile.my_secretaries.through.objects.filter(
                        consultantprofile_id=channel[0].consultant.id, userprofile_id=request.user.id)) != 0:
                    return Response({"error": "You are secretary of this channel!!!"},
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
            query = request.GET['query']  # string

            if request.GET.get('search_category') != None:
                search_caregory = request.GET['search_category']
            data = []
            if request.GET.get('search_category') != None:
                #  ch = Channel.objects.filter(consultant==)
                Channels = Channel.objects.filter(consultant__user_type=search_caregory).filter(
                    Q(name__icontains=query) | Q(description__icontains=query))
                for channel in Channels:
                    data.append({
                        'name': channel.name,
                        'consultant_full_name': channel.consultant.first_name + " " + channel.consultant.last_name,
                        'invite_link': channel.invite_link,
                    })
            else:
                Channels = Channel.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
                for channel in Channels:
                    data.append({
                        'name': channel.name,
                        'consultant_full_name': channel.consultant.first_name + " " + channel.consultant.last_name,
                        'invite_link': channel.invite_link,
                    })

            return Response({'data': data}, status=status.HTTP_200_OK)
        except:
            return Response({'status': "Internal Server Error, We'll Check it later!"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SuggestionChannel(APIView):
    permission_classes = []

    def get(self, request, format=None):
        try:
            data = []
            Channels = Channel.objects.all()[0:10]
            for channel in Channels:
                data.append({
                    'name': channel.name,
                    'consultant_full_name': channel.consultant.first_name + " " + channel.consultant.last_name,
                    'invite_link': channel.invite_link,
                })
            return Response({'data': data}, status=status.HTTP_200_OK)
        except:
            return Response({'status': "Internal Server Error, We'll Check it later!"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetChannelSubscribers(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            channel_url_or_id = request.GET['channel-url']  # string
            channel_ = Channel.objects.filter(invite_link=channel_url_or_id)
            if len(channel_) == 0:
                return Response("channel not exist!", status=status.HTTP_404_NOT_FOUND)
            channel_ = channel_[0]
            if channel_.consultant.id != request.user.id and (
                    request.user not in UserProfile.objects.filter(consultantprofile=channel_.consultant)):
                return Response("You do not have permission to perform this action", status=status.HTTP_403_FORBIDDEN)
            sb = Subscription.objects.filter(channel=channel_)
            data = []
            for i in range(len(sb)):
                data.append({
                    'name': sb[i].user.email,
                    'username': sb[i].user.username,
                    'user_type': sb[i].user.user_type,
                    'avatar': sb[i].user.avatar if sb[i].user.avatar else None,
                })
            return Response({'data': data}, status=status.HTTP_200_OK)
        except:
            return Response({'status': "Internal Server Error, We'll Check it later!"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetChannelAdmins(APIView):
    permission_classes = []

    def get(self, request, format=None):
        try:
            channel_url_or_id = request.GET['channel-url']  # string
            channel_ = Channel.objects.filter(invite_link=channel_url_or_id)
            if len(channel_) == 0:
                return Response("channel not exist!", status=status.HTTP_404_NOT_FOUND)
            channel_ = channel_[0]
            # if channel_.consultant.id != request.user.id and ( request.user not in UserProfile.objects.filter(consultantprofile=channel_.consultant)):
            #   return Response("You do not have permission to perform this action", status=status.HTTP_403_FORBIDDEN)

            admins = UserProfile.objects.filter(consultantprofile=channel_.consultant)
            print(admins)
            data = []
            for i in range(len(admins)):
                data.append({
                    'name': admins[i].user.email,
                    'username': admins[i].user.username,
                    'user_type': admins[i].user.user_type,
                    'avatar': admins[i].user.avatar if admins[i].user.avatar else None,
                })
            main_data = {
                'admin': data,
                'consultant': {
                    'name': channel_.consultant.email,
                    'username': channel_.consultant.username,
                    'user_type': channel_.consultant.user_type,
                    'avatar': channel_.consultant.avatar if channel_.consultant.avatar else None,
                }
            }
            return Response({'data': main_data}, status=status.HTTP_200_OK)
        except:
            return Response({'status': "Internal Server Error, We'll Check it later!"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
