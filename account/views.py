from rest_framework import generics, status
from .models import CustomUser
from .serializers import CustomUserSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.shortcuts import render

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


