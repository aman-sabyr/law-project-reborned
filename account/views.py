from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *


class RegistrationView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegistrationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.validated_data)
            return Response('<><><><><><> dude account was created alles ist gut <><><><><><>', 200)


class ActivationView(APIView):
    def post(self, request):
        data = request.data
        serializer = ActivationSerializer(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.activate(serializer.validated_data)
            return Response('<><><><><><> dude u activated ur account <><><><><><>', 200)


class LoginView(ObtainAuthToken, APIView):
    """
        ObtainAuthToken has "post" method, and i a little modified it
        As soon as a token is created, it is saved in the user's cookie
    """
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('<><><><><><> dude ur passed out :)) <><><><><><>')
