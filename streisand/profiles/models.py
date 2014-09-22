# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.db import models

from django_extensions.db.fields import UUIDField


class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', related_name='profile')
    auth_key = UUIDField(auto=True, unique=True, editable=False, db_index=True)
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
                  "announces made by this user's torrent client(s)."
    )

    @property
    def username(self):
        return self.user.username

    @property
    def email(self):
        return self.user.email

    @property
    def ratio(self):
        return round(self.bytes_uploaded / self.bytes_downloaded, 3)

    def get_absolute_url(self):
        return reverse('user_profile', args=[self.id])


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
    last_announce = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['profile', 'torrent']
        index_together = ['profile', 'torrent']


class UserIPAddress(models.Model):
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
