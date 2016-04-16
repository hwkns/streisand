# -*- coding: utf-8 -*-

from django.contrib.auth.models import User, Permission
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from profiles.models import UserProfile


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
        user = kwargs['instance']
        UserProfile.objects.create(user=user)
        can_leech = Permission.objects.get(codename='can_leech')
        user.user_permissions.add(can_leech)


# Signal handler for new user profiles
@receiver(post_save, sender='profiles.UserProfile')
def set_defaults_for_new_user_profile(**kwargs):
    if kwargs['created']:
        instance = kwargs['instance']
        if instance.announce_key is None:
            instance.reset_announce_key()
