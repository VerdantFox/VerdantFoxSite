from django.db import models
from embed_video.fields import EmbedVideoField


class Video(models.Model):
    name = models.CharField(max_length=20)
    video = EmbedVideoField()

    def __str__(self):
        return f"{self.name}"