# -*- coding: utf-8 -*-

from django_extensions.db.fields import UUIDField

from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import signals
from django.db.models.aggregates import Sum
from django.dispatch import receiver

from tracker.models import Peer


class UserProfile(models.Model):

    CACHE_KEY = 'user_profile:{user_id}'

    user = models.OneToOneField('auth.User', related_name='profile')
    auth_key = models.OneToOneField(
        'profiles.UserAuthKey',
        related_name='profile',
        null=True,
        default=None,
        editable=False,
        db_index=True,
    )
    invited_by = models.ForeignKey('profiles.UserProfile', null=True)
    bytes_uploaded = models.BigIntegerField(default=0)
    bytes_downloaded = models.BigIntegerField(default=0)
    torrents = models.ManyToManyField(
        'torrents.Torrent',
        through='profiles.TorrentStats',
        related_name='profiles',
    )
    log_successful_announces = models.BooleanField(
        default=False,
        help_text="Use sparingly! This logs data from all successful "
                  "announces made by this user's torrent client(s).",
    )
    watch_queue = models.ForeignKey(
        'film_lists.FilmList',
        null=True,
        blank=True,
        editable=False,
    )

    def __str__(self):
        return self.username

    @property
    def username(self):
        return self.user.username

    @property
    def email(self):
        return self.user.email

    @property
    def ratio(self):
        if self.bytes_downloaded == 0:
            return 0.0
        else:
            return round(self.bytes_uploaded / self.bytes_downloaded, 3)

    @property
    def seeding_size(self):
        seeding_size = Peer.objects.seeders().filter(
            user_auth_key=self.auth_key_id,
        ).aggregate(
            Sum('swarm__torrent__size_in_bytes')
        )['swarm__torrent__size_in_bytes__sum']

        if seeding_size:
            return seeding_size
        else:
            return 0

    def get_absolute_url(self):
        return reverse('user_profile', args=[self.id])

    def reset_auth_key(self):
        self.auth_key = self.auth_keys.create()
        self.save()


# Signal handler for new users
@receiver(models.signals.post_save, sender='auth.User')
def create_profile_for_new_user(sender, instance, created=False, **kwargs):
    if created is True and not hasattr(instance, 'profile'):
        UserProfile.objects.create(user=instance)


# Signal handler for new user profiles
@receiver(models.signals.post_save, sender='profiles.UserProfile')
def set_auth_key_for_new_user_profile(sender, instance, created=False, **kwargs):
    if created is True and instance.auth_key is None:
        instance.reset_auth_key()


class TorrentStats(models.Model):

    # Because Django does not support compound primary keys, and because this
    # table might actually hit the max limit of an auto-incrementing integer ID,
    # we use an auto-generated UUIDField as the primary key.
    id = UUIDField(auto=True, primary_key=True, editable=False)

    profile = models.ForeignKey('profiles.UserProfile', null=False, related_name='torrent_stats')
    torrent = models.ForeignKey('torrents.Torrent', null=False)
    bytes_uploaded = models.BigIntegerField(default=0)
    bytes_downloaded = models.BigIntegerField(default=0)
    snatch_count = models.IntegerField(default=0)
    last_seeded = models.DateTimeField(null=True)

    class Meta:
        unique_together = ['profile', 'torrent']
        index_together = ['profile', 'torrent']


class UserIPAddress(models.Model):
    """
    Used to keep a history of IP addresses used by a profile, including
    both site and tracker interactions.
    """
    profile = models.ForeignKey(
        'profiles.UserProfile',
        null=False,
        db_index=True,
        related_name='ip_addresses',
    )
    ip_address = models.GenericIPAddressField(null=False)
    used_with = models.CharField(max_length=16, null=False)
    first_used = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['profile', 'ip_address', 'used_with']
        index_together = ['profile', 'ip_address', 'used_with']


class UserAuthKey(models.Model):
    """
    Used to keep a history of auth keys used by a profile.
    """
    id = UUIDField(auto=True, primary_key=True)
    used_with_profile = models.ForeignKey(
        'profiles.UserProfile',
        related_name='auth_keys',
        db_index=True,
    )
    used_since = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.__str__()


class UserAnnounce(models.Model):
    """
    Used to keep a record of successful announces for a given user profile.
    """

    # Because Django does not support compound primary keys, and because this
    # table might actually hit the max limit of an auto-incrementing integer ID,
    # we use an auto-generated UUIDField as the primary key.
    id = UUIDField(auto=True, primary_key=True, editable=False)

    profile = models.ForeignKey(
        'profiles.UserProfile',
        null=False,
        db_index=True,
        related_name='logged_announces',
    )
    time_stamp = models.DateTimeField(null=False)
    auth_key = UUIDField(auto=False, null=False)
    info_hash = models.CharField(max_length=40, db_index=True, null=False)
    ip_address = models.GenericIPAddressField(null=False)
    port = models.IntegerField(null=False)
    peer_id = models.CharField(max_length=40, null=False)
    user_agent = models.TextField(null=False)
    new_bytes_uploaded = models.BigIntegerField(default=0, null=False)
    new_bytes_downloaded = models.BigIntegerField(default=0, null=False)
    bytes_remaining = models.BigIntegerField(null=False)
    event = models.CharField(max_length=16, null=False)


def invalidate_user_cache(sender, instance, **kwargs):
    if sender == User:
        key = UserProfile.CACHE_KEY.format(user_id=instance.id)
    else:
        key = UserProfile.CACHE_KEY.format(user_id=instance.user_id)
    cache.delete(key)


signals.post_save.connect(invalidate_user_cache, sender=User)
signals.post_save.connect(invalidate_user_cache, sender=UserProfile)
signals.post_delete.connect(invalidate_user_cache, sender=User)
signals.post_delete.connect(invalidate_user_cache, sender=UserProfile)
