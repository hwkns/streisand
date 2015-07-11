# -*- coding: utf-8 -*-

from django.db import models

from .managers import FeatureManager


class Feature(models.Model):

    name = models.CharField(max_length=128, primary_key=True)
    description = models.TextField()
    is_enabled = models.BooleanField(default=False)

    objects = FeatureManager()
