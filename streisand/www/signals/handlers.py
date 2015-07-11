# -*- coding: utf-8 -*-

from django.db import models
from django.dispatch import receiver

from www.models import Feature


@receiver(models.signals.post_save, sender='www.Feature')
@receiver(models.signals.post_delete, sender='www.Feature')
def invalidate_feature_cache(**kwargs):
    """
    When Feature objects are saved or deleted, invalidate their
    cache entries.
    """
    feature = kwargs['instance']
    Feature.objects.invalidate_cache(feature.name)
