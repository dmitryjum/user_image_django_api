from rest_framework import serializers
from .models import PublicUser, Image
class PublicUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = PublicUser
    fields = ['id', 'username', 'email', 'password']
    extra_kwargs = {'password': {'write_only': True}}

  def create(self, validated_data):
    user = PublicUser.objects.create_user(
          username=validated_data['username'],
          email=validated_data['email'],
          password=validated_data['password']
    )
    return user
      
    
class ImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = Image
    fields = ['id', 'author', 'width', 'height', 'url', 'download_url']