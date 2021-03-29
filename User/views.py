from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers


from .models import *


class SwaggerUI(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'swagger-ui.html')


class UserSignupAPI(APIView):

    def post(self, request, format=None):
        try:
            serializer = serializers.UserSignupSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return_data = serializers.UserConsultantSerializerReturnData(data=serializer.validated_data)
                return_data.is_valid(raise_exception=True)
                return Response(data=return_data.validated_data, status=status.HTTP_200_OK)
            else:
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserConsultantLoginAPI(APIView):
    def post(self, request):
        try:
            serializer = serializers.UserConsultantLoginSerializer(data=request.data)
            if serializer.is_valid():
                # TODO: WRITE NATIVE QUERY HERE , USERNAME OR EMAIL
                user = list(UserProfile.objects.filter(username=serializer.validated_data['email_username']))
                if len(user) == 0:
                    user = UserProfile.objects.filter(email=serializer.validated_data['email_username'])
                if len(user) == 0:
                    return Response({'error': 'This user not found'}, status=status.HTTP_400_BAD_REQUEST)
                return_data = serializers.UserConsultantSerializerReturnData(user[0], many=False, partial=True)
                return Response(data=return_data.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConsultantSignupAPI(APIView):

    def post(self, request, format=None):
        try:
            if request.data['consultant_type'] == 'Lawyer':
                serializer = serializers.LawyerSignupSerializer(data=request.data)
            else:
                return Response({'error': 'Type of consultant is not valid!!'}, status=status.HTTP_400_BAD_REQUEST)
            if serializer.is_valid():
                serializer.save()
                return_data = serializers.UserConsultantSerializerReturnData(data=serializer.validated_data)
                return_data.is_valid(raise_exception=True)
                return Response(data=return_data.validated_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as server_error:
            return Response(server_error.__str__(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
