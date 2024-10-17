import pdb
import requests
from django.core.management.base import BaseCommand
from images_api.models import Image
from decouple import config

class Command(BaseCommand):
  help = 'Seed the database with images'

  def handle(self, *args, **kwargs):
    url = config('IMAGE_SEED_URL')
    response = requests.get(url)
    if response.status_code == 200:
        images = response.json()
        for image_data in images:
            Image.objects.get_or_create(
                id=image_data['id'],
                defaults={
                    'author': image_data['author'],
                    'width': image_data['width'],
                    'height': image_data['height'],
                    'url': image_data['url'],
                    'download_url': image_data['download_url']
                }
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(images)} images'))
    else:
        self.stdout.write(self.style.ERROR('Failed to fetch images from the URL'))