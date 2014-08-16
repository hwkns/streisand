from django.contrib.auth.models import User
from django.db import models

from django_extensions.db.fields import UUIDField


class Profile(models.Model):
    user = models.OneToOneField(User)
    auth_key = UUIDField(unique=True, max_length=64)
    bytes_uploaded = models.BigIntegerField(default=0)
    bytes_downloaded = models.BigIntegerField(default=0)
