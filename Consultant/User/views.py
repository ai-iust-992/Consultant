from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UserLoginAPI(APIView):
    def get(self, request, format=None):
        return Response({'data': 'nothing in user'}, status=status.HTTP_200_OK)


class ConsultantLoginAPI(APIView):
    def get(self, request, format=None):
        return Response({'data': 'nothing in consultant'}, status=status.HTTP_200_OK)
