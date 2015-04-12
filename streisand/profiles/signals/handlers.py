# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from profiles.models import UserProfile, WatchedUser, LoginAttempt


@receiver(user_login_failed)
def track_failed_login_attempts(**kwargs):

    if kwargs['sender'] == 'django.contrib.auth':

        username = kwargs['credentials']['username']

        try:
            user = User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            pass
        else:
            LoginAttempt.objects.create(
                user=user,
                success=False,
            )


@receiver(user_logged_in)
def track_successful_login_attempts(**kwargs):

    user = kwargs['user']

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
        success=True,
    )


@receiver([post_save, post_delete], sender=User)
@receiver([post_save, post_delete], sender=UserProfile)
def invalidate_user_cache(**kwargs):
    instance = kwargs['instance']
    if kwargs['sender'] == User:
        key = UserProfile.CACHE_KEY.format(user_id=instance.id)
    else:
        key = UserProfile.CACHE_KEY.format(user_id=instance.user_id)
    cache.delete(key)


# Signal handler for new users
@receiver(post_save, sender='auth.User')
def create_profile_for_new_user(**kwargs):
    if kwargs['created']:
        UserProfile.objects.create(user=kwargs['instance'])


# Signal handler for new user profiles
@receiver(post_save, sender='profiles.UserProfile')
def set_announce_key_for_new_user_profile(**kwargs):
    if kwargs['created']:
        instance = kwargs['instance']
        if instance.announce_key is None:
            instance.reset_announce_key()
