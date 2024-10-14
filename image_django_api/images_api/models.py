from django.contrib.auth.models import AbstractUser
from django.db import models


class PublicUser(AbstractUser):
  pass

  def __str__(self):
        return self.username
  
class Image(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    author = models.CharField(max_length=100)
    width = models.IntegerField()
    height = models.IntegerField()
    url = models.URLField()
    download_url = models.URLField()

    def __str__(self):
        return f"Image {self.id} by {self.author}"