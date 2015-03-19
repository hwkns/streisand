# -*- coding: utf-8 -*-

from decimal import Decimal

from django_extensions.db.fields import UUIDField

from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.db import models, transaction
from django.db.models import signals
from django.db.models.aggregates import Sum
from django.dispatch import receiver
from django.utils.timezone import now

from tracker.models import Peer


class UserProfile(models.Model):

    CACHE_KEY = 'user_profile:{user_id}'

    STATUS_CHOICES = (
        ('unconfirmed', 'Unconfirmed'),
        ('enabled', 'Enabled'),
        ('disabled', 'Disabled'),
    )

    old_id = models.PositiveIntegerField(null=True, db_index=True)

    user = models.OneToOneField('auth.User', related_name='profile')
    account_status = models.CharField(max_length=32, choices=STATUS_CHOICES, db_index=True)
    announce_key = models.OneToOneField(
        'profiles.UserAnnounceKey',
        related_name='profile',
        null=True,
        default=None,
        editable=False,
        db_index=True,
        on_delete=models.SET_NULL,
    )
    avatar_url = models.URLField()
    custom_title = models.CharField(max_length=256, null=True)
    staff_notes = models.TextField()
    irc_key = models.CharField(max_length=128)
    invited_by = models.ForeignKey(
        'profiles.UserProfile',
        null=True,
        on_delete=models.SET_NULL,
    )
    invite_count = models.PositiveIntegerField(default=0)
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
    last_seeded = models.DateTimeField(null=True)
    watch_queue = models.ForeignKey(
        'film_lists.FilmList',
        null=True,
        blank=True,
        editable=False,
        on_delete=models.SET_NULL,
    )

    class Meta:
        permissions = (
            ('can_invite', "Can invite new users"),
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
    def announce_url(self):
        return settings.ANNOUNCE_URL_TEMPLATE.format(announce_key=self.announce_key_id)

    @property
    def ratio(self):
        if self.bytes_downloaded == 0:
            return 0.0
        else:
            return round(self.bytes_uploaded / self.bytes_downloaded, 3)

    @property
    def seeding_size(self):
        seeding_size = Peer.objects.seeders().filter(
            user_announce_key=self.announce_key_id,
        ).aggregate(
            Sum('swarm__torrent__size_in_bytes')
        )['swarm__torrent__size_in_bytes__sum']

        if seeding_size:
            return seeding_size
        else:
            return 0

    @property
    def admin_link(self):
        return '<a href="{profile_url}">{username}</a>'.format(
            profile_url=reverse('admin:profiles_userprofile_change', args=[self.id]),
            username=self.username,
        )

    def get_absolute_url(self):
        return reverse('user_profile', args=[self.username])

    def reset_announce_key(self):

        with transaction.atomic():

            # Revoke old key
            if self.announce_key_id:
                old_key = self.announce_key
                old_key.revoked_at = now()
                old_key.save()

            # Issue new key
            self.announce_key = self.announce_keys.create()
            self.save()


# Signal handler for new users
@receiver(models.signals.post_save, sender='auth.User')
def create_profile_for_new_user(sender, instance, created=False, **kwargs):
    if created is True and not hasattr(instance, 'profile'):
        UserProfile.objects.create(user=instance)


# Signal handler for new user profiles
@receiver(models.signals.post_save, sender='profiles.UserProfile')
def set_announce_key_for_new_user_profile(sender, instance, created=False, **kwargs):
    if created is True and instance.announce_key is None:
        instance.reset_announce_key()


class TorrentStats(models.Model):

    # Because Django does not support compound primary keys, and because this
    # table might actually hit the max limit of an auto-incrementing integer ID,
    # we use an auto-generated UUIDField as the primary key.
    id = UUIDField(auto=True, primary_key=True, editable=False)

    profile = models.ForeignKey(
        'profiles.UserProfile',
        null=False,
        related_name='torrent_stats',
    )
    torrent = models.ForeignKey(
        'torrents.Torrent',
        null=False,
        related_name='torrent_stats',
    )
    download_multiplier = models.DecimalField(default=Decimal(1.0), decimal_places=2, max_digits=6)
    upload_multiplier = models.DecimalField(default=Decimal(1.0), decimal_places=2, max_digits=6)
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


class UserAnnounceKey(models.Model):
    """
    Used to keep a history of auth keys used by a profile.
    """
    id = UUIDField(auto=True, primary_key=True)
    used_with_profile = models.ForeignKey(
        'profiles.UserProfile',
        related_name='announce_keys',
        db_index=True,
    )
    issued_at = models.DateTimeField(auto_now_add=True)
    revoked_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.id


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
    swarm = models.ForeignKey(
        'tracker.Swarm',
        null=False,
        db_index=True,
    )
    time_stamp = models.DateTimeField(null=False)
    announce_key = UUIDField(auto=False, null=False)
    ip_address = models.GenericIPAddressField(null=False)
    port = models.IntegerField(null=False)
    peer_id = models.CharField(max_length=40, null=False)
    user_agent = models.TextField(null=False)
    new_bytes_uploaded = models.BigIntegerField(default=0, null=False)
    new_bytes_downloaded = models.BigIntegerField(default=0, null=False)
    bytes_remaining = models.BigIntegerField(null=False)
    event = models.CharField(max_length=16, null=False)


class WatchedUser(models.Model):

    profile = models.ForeignKey('profiles.UserProfile')
    notes = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    last_checked = models.DateTimeField(auto_now=True)
    checked_by = models.ForeignKey('auth.User')


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
