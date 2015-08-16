# -*- coding: utf-8 -*-

from django.db import models

from .managers import FeatureManager


class Feature(models.Model):

    name = models.CharField(max_length=128, primary_key=True)
    description = models.TextField()
    is_enabled = models.BooleanField(default=False)

    objects = FeatureManager()


class LogEntry(models.Model):

    ACTION_CHOICES = (
        'torrent_uploaded',
        'torrent_edited',
        'torrent_deleted',
        'user_created',
        'user_deleted',
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    action = models.CharField(max_length=128, db_index=True)
    text = models.CharField(max_length=1024)
