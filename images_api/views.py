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
  
class ImageListView(generics.ListAPIView):
  serializer_class = ImageSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
      queryset = Image.objects.all()
      author = self.request.query_params.get('author')
      max_width = self.request.query_params.get('maxWidth')
      max_height = self.request.query_params.get('maxHeight')

      if author:
          queryset = queryset.filter(author__iexact=author)

      if max_width:
          queryset = queryset.filter(width__lte=max_width)

      if max_height:
          queryset = queryset.filter(height__lte=max_height)

      return queryset