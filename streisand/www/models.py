# -*- coding: utf-8 -*-

from django.db import models
from django.dispatch import receiver

from .managers import FeatureManager


class Feature(models.Model):

    name = models.CharField(max_length=128, primary_key=True)
    description = models.TextField()
    is_enabled = models.BooleanField(default=False)

    objects = FeatureManager()


@receiver(models.signals.post_save, sender='www.Feature')
@receiver(models.signals.post_delete, sender='www.Feature')
def invalidate_feature_cache(sender, instance, **kwargs):
    """
    When Feature objects are saved or deleted, invalidate their
    cache entries.
    """
    Feature.objects.invalidate_cache(instance.name)
