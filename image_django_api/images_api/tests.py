import pdb
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import PublicUser, Image

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
    PublicUser.objects.create_user(username = 'testuser', email = 'testuser@example.com', password = 'testpassword123')
    data = {
      'username': 'testuser',
      'password': 'testpassword123'
    }
    response = self.client.post(self.login_url, data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIn('token', response.data)

class ImageRetrievalTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = PublicUser.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.list_url = reverse('image-list')

        Image.objects.create(id='1', author='Author1', width=100, height=100, url='http://example.com/1', download_url='http://example.com/1/download')
        Image.objects.create(id='2', author='Author2', width=200, height=200, url='http://example.com/2', download_url='http://example.com/2/download')
        Image.objects.create(id='3', author='Author1', width=300, height=300, url='http://example.com/3', download_url='http://example.com/3/download')

    def test_get_all_images(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_filter_by_author(self):
        response = self.client.get(f'{self.list_url}?author=Author1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_max_width(self):
        response = self.client.get(f'{self.list_url}?maxWidth=150')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_max_height(self):
        response = self.client.get(f'{self.list_url}?maxHeight=250')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_no_results_by_author(self):
        response = self.client.get(f'{self.list_url}?author=NonexistentAuthor')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_filter_no_results_by_max_width(self):
        response = self.client.get(f'{self.list_url}?maxWidth=50')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_filter_no_results_by_max_height(self):
        response = self.client.get(f'{self.list_url}?maxHeight=50')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_unauthenticated_access(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
