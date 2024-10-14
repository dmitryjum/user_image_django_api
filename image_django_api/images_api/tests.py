from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import PublicUser

class UserAuthTests(TestCase):
  def setUp(self):
    self.client = APIClient()
    self.register_url = reverse('register')
    self.login_url = reverse('login')

  def test_user_registration(self):
    data = {
      'username': 'testuser',
      'email': 'testuser@example.com',
      'password': 'testpassword123'
    }
    response = self.client.post(self.register_url, data)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(PublicUser.objects.count(), 1)
    self.assertEqual(PublicUser.objects.get().username, 'testuser')

  def test_user_login(self):
    user = PublicUser.objects.create_user(username = 'testuser', email = 'testuser@example.com', password = 'testpassword123')
    data = {
      'username': 'testuser',
      'password': 'testpassword123'
    }
    response = self.client.post(self.login_url, data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIn('token', response.data)
