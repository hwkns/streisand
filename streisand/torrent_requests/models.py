# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.db import models


class TorrentRequest(models.Model):

    ANY = 'any'
    ANY_CHOICE = (ANY, 'ANY')

    # Site information
    creator = models.ForeignKey('profiles.UserProfile', related_name='torrent_requests')
    film = models.ForeignKey('films.Film', related_name='torrent_requests')
    description = models.TextField()

    # Format information
    is_source = models.BooleanField(default=False)
    source_media = models.ForeignKey('media_formats.SourceMedia', null=True, related_name='torrent_requests')
    resolution = models.ForeignKey('media_formats.Resolution', null=True, related_name='torrent_requests')
    codec = models.ForeignKey('media_formats.Codec', null=True, related_name='torrent_requests')
    container = models.ForeignKey('media_formats.Container', null=True, related_name='torrent_requests')

    def __str__(self):
        return '{film} - {codec} / {container} / {resolution} / {source_media}'.format(
            film=self.film,
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
