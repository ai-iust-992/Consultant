from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from . import serializers
from django.views.generic import TemplateView

from .models import *
from .serializers import RequestSerializer, AnswerSerializer


class SwaggerUI(TemplateView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return render(request, 'swagger-ui.html')


class UserSignupAPI(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        try:
            serializer = serializers.UserSignupSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return_data = serializers.UserConsultantSerializerReturnData(data=serializer.validated_data)
                return_data.is_valid(raise_exception=True)
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'data': return_data.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserConsultantLoginAPI(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = serializers.UserConsultantLoginSerializer(data=request.data)
            if serializer.is_valid():
                # TODO: WRITE NATIVE QUERY HERE , USERNAME OR EMAIL
                user = list(BaseUser.objects.filter(username=serializer.validated_data['email_username']))
                if len(user) == 0:
                    user = BaseUser.objects.filter(email=serializer.validated_data['email_username'])
                if len(user) == 0:
                    return Response({'error': 'This user not found'}, status=status.HTTP_400_BAD_REQUEST)
                if user[0].password != serializer.validated_data['password']:
                    return Response({'error': 'The password is not true'}, status=status.HTTP_400_BAD_REQUEST)
                return_data = serializers.UserConsultantSerializerReturnData(user[0], many=False, partial=True)

                token, created = Token.objects.get_or_create(user=user[0])
                return Response({
                    'token': token.key,
                    'data': return_data.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConsultantSignupAPI(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        try:
            serializer = serializers.ConsultanSignupSerializer(data=request.data)

            if serializer.is_valid():
                user = serializer.save()
                return_data = serializers.UserConsultantSerializerReturnData(data=serializer.validated_data)
                return_data.is_valid(raise_exception=True)

                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'data': return_data.data,
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            secretary_requests = Request.objects.filter(consultant=consultant[0])
            return Response(AnswerSerializer(secretary_requests, many=True).data, status=status.HTTP_200_OK)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, requestId, format=None):
        try:
            consultant = ConsultantProfile.objects.filter(baseuser_ptr_id=request.user.id)
            if len(consultant) == 0:
                return Response("You do not have permission to perform this action", status=status.HTTP_403_FORBIDDEN)
            secretary_requests = Request.objects.filter(consultant=consultant[0], id=requestId)
            if len(secretary_requests) == 0:
                return Response("RequestId is not valid", status=status.HTTP_403_FORBIDDEN)
            secretary_requests.delete()
            return Response("request is deleted", status=status.HTTP_200_OK)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
