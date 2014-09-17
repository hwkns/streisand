# -*- coding: utf-8 -*-

from django.db import models

from django_extensions.db.fields import UUIDField


class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', related_name='profile')
    auth_key = UUIDField(unique=True, max_length=36)
    bytes_uploaded = models.BigIntegerField(default=0)
    bytes_downloaded = models.BigIntegerField(default=0)
    torrents = models.ManyToManyField('torrents.Torrent', through='profiles.TorrentStats')


class TorrentStats(models.Model):
    profile = models.ForeignKey('profiles.UserProfile')
    torrent = models.ForeignKey('torrents.Torrent')
    bytes_uploaded = models.BigIntegerField(default=0)
    bytes_downloaded = models.BigIntegerField(default=0)
    snatch_count = models.IntegerField(default=0)
