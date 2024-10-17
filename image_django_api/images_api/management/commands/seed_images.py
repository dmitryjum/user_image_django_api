import pdb
import requests
from django.core.management.base import BaseCommand
from images_api.models import Image
from decouple import config
from pgbulk import upsert

class Command(BaseCommand):
  help = 'Seed the database with images'

  def handle(self, *args, **kwargs):
    url = config('IMAGE_SEED_URL')
    response = requests.get(url)
    if response.status_code == 200:
        images = response.json()
        data = [
            Image(
                id=image['id'],
                author=image['author'],
                width=image['width'],
                height=image['height'],
                url=image['url'],
                download_url=image['download_url']
            )
            for image in images
        ]
        # Perform bulk upsert
        upsert(
            Image,
            data,
            ["id"],  # Unique constraint fields
            ["author", "width", "height", "url", "download_url"],  # Fields to update
            returning=True  # Optional: return the results of the upsert
        )
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(images)} images'))
    else:
        self.stdout.write(self.style.ERROR('Failed to fetch images from the URL'))