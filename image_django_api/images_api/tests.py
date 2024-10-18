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
        self.create_images(20)

    def create_images(self, count):
      images_data = [
          {'id': 1, 'author': 'Author1', 'width': 100, 'height': 100, 'url': 'http://example.com/1', 'download_url': 'http://example.com/1/download'},
          {'id': 2, 'author': 'Author1', 'width': 110, 'height': 110, 'url': 'http://example.com/2', 'download_url': 'http://example.com/2/download'},
          {'id': 3, 'author': 'Author2', 'width': 120, 'height': 120, 'url': 'http://example.com/3', 'download_url': 'http://example.com/3/download'},
          {'id': 4, 'author': 'Author2', 'width': 130, 'height': 130, 'url': 'http://example.com/4', 'download_url': 'http://example.com/4/download'},
          {'id': 5, 'author': 'Author3', 'width': 140, 'height': 140, 'url': 'http://example.com/5', 'download_url': 'http://example.com/5/download'},
          {'id': 6, 'author': 'Author3', 'width': 150, 'height': 150, 'url': 'http://example.com/6', 'download_url': 'http://example.com/6/download'},
          {'id': 7, 'author': 'Author4', 'width': 160, 'height': 160, 'url': 'http://example.com/7', 'download_url': 'http://example.com/7/download'},
          {'id': 8, 'author': 'Author4', 'width': 170, 'height': 170, 'url': 'http://example.com/8', 'download_url': 'http://example.com/8/download'},
          {'id': 9, 'author': 'Author5', 'width': 180, 'height': 180, 'url': 'http://example.com/9', 'download_url': 'http://example.com/9/download'},
          {'id': 10, 'author': 'Author5', 'width': 190, 'height': 190, 'url': 'http://example.com/10', 'download_url': 'http://example.com/10/download'},
          {'id': 11, 'author': 'Author1', 'width': 200, 'height': 200, 'url': 'http://example.com/11', 'download_url': 'http://example.com/11/download'},
      ]

      # Create images in bulk
      for image_data in images_data:
          Image.objects.create(**image_data)

    def test_get_the_first_page(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 11)
        self.assertEqual(len(response.data['results']), 10)

    def test_get_the_second_page(self):
        response = self.client.get(f'{self.list_url}?page=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 11)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_by_author(self):
        response = self.client.get(f'{self.list_url}?author=Author1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

    def test_filter_by_max_width(self):
        response = self.client.get(f'{self.list_url}?maxWidth=150')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 6)

    def test_filter_by_max_height(self):
        response = self.client.get(f'{self.list_url}?maxHeight=190')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)

    def test_filter_no_results_by_author(self):
        response = self.client.get(f'{self.list_url}?author=NonexistentAuthor')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(response.data['results'], [])

    def test_filter_no_results_by_max_width(self):
        response = self.client.get(f'{self.list_url}?maxWidth=50')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])

    def test_filter_no_results_by_max_height(self):
        response = self.client.get(f'{self.list_url}?maxHeight=50')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])

    def test_unauthenticated_access(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
