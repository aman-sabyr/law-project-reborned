from django.shortcuts import render
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *


class RegistrationView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        data = request.data
        serializer = RegistrationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.validated_data)
            return Response('<><><><><><> dude account was created alles ist gut <><><><><><>', 200)


class ActivationView(generics.GenericAPIView):
    serializer_class = ActivationSerializer

    def post(self, request):
        data = request.data
        serializer = ActivationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.activate(serializer.validated_data)
            return Response('<><><><><><> dude u activated ur account <><><><><><>', 201)


class LoginView(ObtainAuthToken, APIView):

    serializer_class = LoginSerializer


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('<><><><><><> dude ur passed out :)) <><><><><><>')
