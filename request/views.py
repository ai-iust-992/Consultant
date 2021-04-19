from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from User.models import ConsultantProfile, BaseUser
from channel.models import Channel
from request.serializers import RequestSerializer, AnswerSerializer, Request


class SecretaryRequestAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            consultant = ConsultantProfile.objects.filter(baseuser_ptr_id=request.user.id)
            if len(consultant) == 0:
                return Response("You do not have permission to perform this action", status=status.HTTP_403_FORBIDDEN)
            request_serializer = RequestSerializer(data=request.data)
            if request_serializer.is_valid():
                user = BaseUser.objects.filter(username=request_serializer.validated_data['target_user'])
                if len(user) == 0:
                    return Response({"error": "This username is not valid"}, status=status.HTTP_400_BAD_REQUEST)
                if len(ConsultantProfile.objects.filter(my_secretaries=user[0])) != 0:
                    return Response({"error": "This username is already secretary of you"},
                                    status=status.HTTP_400_BAD_REQUEST)
                request_serializer.validated_data['consultant'] = consultant[0]
                request_serializer.validated_data['target_user'] = user[0]
                request_serializer.validated_data['request_type'] = 'secretary'
                secretary_request = request_serializer.save()
                return Response(data=AnswerSerializer(secretary_request).data, status=status.HTTP_200_OK)
            else:
                return Response({"error": request_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, format=None):
        try:
            consultant = ConsultantProfile.objects.filter(baseuser_ptr_id=request.user.id)
            if len(consultant) == 0:
                return Response("You do not have permission to perform this action", status=status.HTTP_403_FORBIDDEN)
            secretary_requests = Request.objects.filter(consultant=consultant[0], request_type="secretary").order_by(
                "-id")
            return Response(AnswerSerializer(secretary_requests, many=True).data, status=status.HTTP_200_OK)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, requestId, format=None):
        try:
            consultant = ConsultantProfile.objects.filter(baseuser_ptr_id=request.user.id)
            if len(consultant) == 0:
                return Response("You do not have permission to perform this action", status=status.HTTP_403_FORBIDDEN)
            secretary_request = Request.objects.filter(consultant=consultant[0], id=requestId)
            if len(secretary_request) == 0:
                return Response("RequestId is not valid", status=status.HTTP_400_BAD_REQUEST)
            secretary_request.delete()
            return Response("request is deleted", status=status.HTTP_200_OK)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AnswerToRequestAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, requestId, format=None):
        try:
            user_request = Request.objects.filter(id=requestId, target_user=request.user).select_related(
                "consultant").select_related('target_user')
            if len(user_request) == 0:
                return Response({"error": "RequestId is not valid"}, status=status.HTTP_400_BAD_REQUEST)
            answer_serializer = AnswerSerializer(user_request[0], data=request.data)
            if answer_serializer.is_valid():
                answer_serializer.save()
                if answer_serializer.validated_data['accept']:
                    if answer_serializer.validated_data['request_type'] == "secretary":
                        user_request[0].consultant.my_secretaries.add(request.user)
                    elif answer_serializer.validated_data['request_type'] == "join_channel":
                        Channel.objects.filter(consultant=user_request[0].consultant)[0].subscribers.add(request.user)
                return Response(answer_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": answer_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, format=None):
        try:
            user_requests = Request.objects.filter(target_user=request.user).order_by('-id')
            return Response(AnswerSerializer(user_requests, many=True).data, status=status.HTTP_200_OK)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class JoinChannelRequestAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, channelId, format=None):
        try:
            channel = Channel.objects.filter(id=channelId).select_related('consultant')
            if len(channel) == 0:
                return Response("Channel id is not valid", status=status.HTTP_400_BAD_REQUEST)
            if channel[0].consultant.baseuser_ptr_id != request.user.id and len(
                    ConsultantProfile.my_secretaries.through.objects.filter(
                        consultantprofile_id=channel[0].consultant.id, userprofile_id=request.user.id)) == 0:
                return Response({"error": "You dont have permission for this request"},
                                status=status.HTTP_403_FORBIDDEN)
            request_serializer = RequestSerializer(data=request.data)
            if request_serializer.is_valid():
                recipient_request = BaseUser.objects.filter(username=request_serializer.validated_data['target_user'])
                if len(recipient_request) == 0:
                    return Response({"error": "This username is not valid"}, status=status.HTTP_400_BAD_REQUEST)
                if len(Channel.subscribers.through.objects.filter(user=recipient_request[0])) != 0:
                    return Response({"error": "This username is already subscriber of this channel"},
                                    status=status.HTTP_400_BAD_REQUEST)
                request_serializer.validated_data['consultant'] = channel[0].consultant
                request_serializer.validated_data['target_user'] = recipient_request[0]
                join_request = request_serializer.save()
                return Response(data=AnswerSerializer(join_request).data, status=status.HTTP_200_OK)
            else:
                return Response({"error": request_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def get(self, request, format=None):
    #     try:
    #         join_requests = Request.objects.filter()
    #         if len(consultant) == 0:
    #             return Response("Channel id is not valid", status=status.HTTP_400_BAD_REQUEST)
    #         if channel[0].consultant.baseuser_ptr_id != request.user.id and len(
    #                 ConsultantProfile.my_secretaries.through.objects.filter(
    #                     consultantprofile_id=channel[0].consultant.id, userprofile_id=request.user.id)) == 0:
    #             return Response({"error": "You dont have permission for this request"},
    #                             status=status.HTTP_403_FORBIDDEN)
    #         join_requests = Request.objects.filter(consultant=channel[0].consultant,
    #                                                request_type="join_channel").order_by("-id")
    #         return Response(AnswerSerializer(join_requests, many=True).data, status=status.HTTP_200_OK)
    #     except Exception as server_error:
    #         return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, requestId, format=None):
        try:
            join_request = Request.objects.filter(id=requestId).select_related('consultant')
            if len(join_request) == 0:
                return Response("RequestId is not valid", status=status.HTTP_400_BAD_REQUEST)
            if join_request[0].consultant.baseuser_ptr_id != request.user.id and len(
                    ConsultantProfile.my_secretaries.through.objects.filter(
                        consultantprofile_id=join_request[0].consultant.id, userprofile_id=request.user.id)) == 0:
                return Response({"error": "You dont have permission for this request"},
                                status=status.HTTP_403_FORBIDDEN)
            join_request.delete()
            return Response("request is deleted", status=status.HTTP_200_OK)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
