from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers


class UserSignupAPI(APIView):
    def post(self, request, format=None):
        try:
            serializer = serializers.UserSignupSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({}, status=status.HTTP_200_OK)
            else:
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'status': 'Internal server error!!!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLoginAPI(APIView):
    def post(self, request):
        pass


class ConsultantSignupAPI(APIView):
    def post(self, request, format=None):
        try:
            if request.data == 'Lawyer':
                serializer = serializers.LawyerSignupSerializer(data=request.data)
            else:
                return Response({'error': 'Type of consultant is not valid!!'}, status=status.HTTP_400_BAD_REQUEST)
            if serializer.is_valid():
                serializer.save()
                return Response({}, status=status.HTTP_200_OK)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'status': 'Internal server error!!!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

