# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver

from profiles.models import WatchedUser

from ..models import Feature, LoginAttempt
from .signals import successful_login, failed_login


@receiver(models.signals.post_save, sender='www.Feature')
@receiver(models.signals.post_delete, sender='www.Feature')
def invalidate_feature_cache(**kwargs):
    """
    When Feature objects are saved or deleted, invalidate their
    cache entries.
    """
    feature = kwargs['instance']
    Feature.objects.invalidate_cache(feature.name)


@receiver(failed_login)
def track_failed_login_attempts(**kwargs):

    username = kwargs['username']
    ip_address = kwargs['ip_address']

    try:
        user = User.objects.get(username__iexact=username)
    except User.DoesNotExist:
        user = None

    LoginAttempt.objects.create(
        user=user,
        username=username,
        ip_address=ip_address,
        success=False,
    )


@receiver(successful_login)
def track_successful_login_attempts(**kwargs):

    user = kwargs['user']
    ip_address = kwargs['ip_address']

    try:
        last_successful_login = user.login_attempts.filter(success=True).latest()
    except LoginAttempt.DoesNotExist:
        failed_login_attempts = user.login_attempts.filter(success=False)
    else:
        failed_login_attempts = user.login_attempts.filter(
            success=False,
            time_stamp__gt=last_successful_login.time_stamp,
        )

    if failed_login_attempts.count() > 2:

        WatchedUser.objects.get_or_create(
            profile=user.profile,
            defaults={
                'notes': '{n} failed login attempts before success'.format(
                    n=failed_login_attempts.count(),
                )
            }
        )

    LoginAttempt.objects.create(
        user=user,
        username=user.username,
        ip_address=ip_address,
        success=True,
    )
