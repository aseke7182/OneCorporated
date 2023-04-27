from django.http import HttpResponse
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


def ping(request):
    return HttpResponse('pong')


class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny, )


class UserLoginAPIView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.data
        user = authenticate(request, email=user['email'], password=user['password'])
        if user is not None:
            login(request, user)
            tokens = RefreshToken.for_user(user)
            data = {
                'access': str(tokens.access_token),
                'refresh': str(tokens),
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response({'message': "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileAPIView(generics.ListAPIView, generics.UpdateAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        profile = self.serializer_class(self.get_object())
        return Response(profile.data, status=status.HTTP_200_OK)
