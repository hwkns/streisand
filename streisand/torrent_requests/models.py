# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.db import models


class TorrentRequest(models.Model):

    # Site information
    created_by = models.ForeignKey('profiles.UserProfile', related_name='torrent_requests')
    film_title = models.CharField(max_length=1024)
    film_year = models.PositiveSmallIntegerField()
    imdb_id = models.CharField(max_length=16, db_index=True)
    description = models.TextField()
    bounty_in_bytes = models.BigIntegerField(default=0)
    filled_with = models.ForeignKey(
        'torrents.Torrent',
        null=True,
        related_name='requests_filled',
        on_delete=models.SET_NULL,
    )

    # Format information
    is_source = models.BooleanField(default=False)
    source_media = models.ForeignKey(
        'media_formats.SourceMedia',
        null=True,
        related_name='torrent_requests',
        on_delete=models.SET_NULL,
    )
    resolution = models.ForeignKey(
        'media_formats.Resolution',
        null=True,
        related_name='torrent_requests',
        on_delete=models.SET_NULL,
    )
    codec = models.ForeignKey(
        'media_formats.Codec',
        null=True,
        related_name='torrent_requests',
        on_delete=models.SET_NULL,
    )
    container = models.ForeignKey(
        'media_formats.Container',
        null=True,
        related_name='torrent_requests',
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return '{film_title} ({year}) - {codec} / {container} / {resolution} / {source_media}'.format(
            film_title=self.film_title,
            year=self.film_year,
            codec=self.codec,
            container=self.container,
            resolution=self.resolution,
            source_media=self.source_media,
        )

    def get_absolute_url(self):
        return reverse(
            viewname='torrent_request_details',
            kwargs={
                'torrent_request_id': self.id,
            }
        )
