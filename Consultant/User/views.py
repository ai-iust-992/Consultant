from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers


class UserLoginAPI(APIView):
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


class ConsultantLoginAPI(APIView):
    def get(self, request, format=None):
        return Response({'data': 'nothing in consultant'}, status=status.HTTP_200_OK)
