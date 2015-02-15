# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.db import models

from picklefield import PickledObjectField


class Torrent(models.Model):

    # Film information
    film = models.ForeignKey('films.Film', null=False, db_index=True, related_name='torrents')
    cut = models.CharField(max_length=128, default='Theatrical')

    # Site information
    uploaded_by = models.ForeignKey('profiles.UserProfile', null=False, related_name='uploaded_torrents')
    encoded_by = models.ForeignKey('profiles.UserProfile', null=True, blank=True, related_name='encodes')
    last_seeded = models.DateTimeField(null=True)
    snatch_count = models.IntegerField(default=0)

    # Release information
    release_name = models.CharField(max_length=1024)
    release_group = models.CharField(max_length=32)
    is_scene = models.NullBooleanField(default=False)

    # Format information
    is_source = models.BooleanField(default=False)
    source_media = models.ForeignKey('media_formats.SourceMedia', related_name='torrents')
    resolution = models.ForeignKey('media_formats.Resolution', related_name='torrents')
    codec = models.ForeignKey('media_formats.Codec', related_name='torrents')
    container = models.ForeignKey('media_formats.Container', related_name='torrents')

    # BitTorrent information
    swarm = models.OneToOneField('tracker.Swarm', related_name='torrent')
    info_hash = models.CharField(max_length=40, db_index=True)
    metadata_dict = PickledObjectField(null=False)
    file_list = PickledObjectField(null=False)
    size_in_bytes = models.BigIntegerField(null=False)

    class Meta:
        permissions = (
            ('upload', "Can upload new torrents"),
        )

    def __str__(self):
        return self.info_hash

    def __repr__(self):
        return self.__str__()

    def get_absolute_url(self):
        return reverse(
            viewname='film_torrent_details',
            kwargs={
                'film_id': self.film_id,
                'torrent_id': self.id,
            }
        )
