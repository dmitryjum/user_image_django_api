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

    class Meta:
        indexes = [
            models.Index(fields=['author'], name='idx_author'),
            models.Index(fields=['width'], name='idx_width'),
            models.Index(fields=['height'], name='idx_height'),
        ]

    def __str__(self):
        return f"Image {self.id} by {self.author}"