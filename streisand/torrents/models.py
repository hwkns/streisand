# -*- coding: utf-8 -*-

from django.db import models


class TorrentGroup(models.Model):
    pass


class Torrent(models.Model):
    swarm = models.OneToOneField('tracker.Swarm', related_name='torrent')
    # uploaded_by = models.ForeignKey('profiles.UserProfile', null=False, related_name='uploaded_torrents')
    # encoded_by = models.ForeignKey('profiles.UserProfile', related_name='encodes')
    group = models.ForeignKey(TorrentGroup, db_index=True)
    info_hash = models.CharField(max_length=40, db_index=True)
    size = models.BigIntegerField(null=False)

    def __str__(self):
        return self.info_hash

    def __repr__(self):
        return self.__str__()
