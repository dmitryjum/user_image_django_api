from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import PublicUser, Image
from .serializers import PublicUserSerializer, ImageSerializer

class RegisterView(generics.CreateAPIView):
  queryset = PublicUser.objects.all()
  permission_classes = (permissions.AllowAny,)
  serializer_class = PublicUserSerializer

class LoginView(generics.CreateAPIView):
  permission_classes = (permissions.AllowAny,)
  serializer_class = PublicUserSerializer

  def create(self, request, *args, **kwargs):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username = username, password = password)
    if user:
      token, _ = Token.objects.get_or_create(user = user)
      return Response({'token': token.key}, status = status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status = status.HTTP_400_BAD_REQUEST)