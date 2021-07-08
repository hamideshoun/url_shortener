import uuid

from django.db import models
from django.contrib.auth.models import User

from URL_Shortener.redis import redis_client


class Url(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, related_name='urls', null=True, blank=True)
    short_url = models.CharField(max_length=20, unique=True)
    main_url = models.URLField()
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Url, self).save(*args, **kwargs)
        redis_client.set(self.short_url, self.main_url)
