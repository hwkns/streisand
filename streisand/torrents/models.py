# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.timezone import now, timedelta

from picklefield import PickledObjectField

from tracker.bencoding import bencode


class Torrent(models.Model):

    old_id = models.PositiveIntegerField(null=True, db_index=True)

    # Film information
    film = models.ForeignKey('films.Film', null=False, db_index=True, related_name='torrents')
    cut = models.CharField(max_length=128, default='Theatrical')

    # Site information
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        to='profiles.UserProfile',
        null=True,
        blank=False,
        related_name='uploaded_torrents',
    )
    encoded_by = models.ForeignKey(
        to='profiles.UserProfile',
        null=True,
        blank=True,
        related_name='encodes',
    )
    moderated_by = models.ForeignKey(
        to='profiles.UserProfile',
        null=True,
        blank=True,
        related_name='moderated_torrents',
    )
    is_approved = models.NullBooleanField(
        choices=(
            (None, 'Not Yet Moderated'),
            (True, 'Approved'),
            (False, 'Work In Progress'),
        )
    )
    last_seeded = models.DateTimeField(null=True)
    reseed_request = models.OneToOneField(
        to='torrents.ReseedRequest',
        null=True,
        related_name='active_on_torrent',
    )
    snatch_count = models.IntegerField(default=0)

    # Release information
    release_name = models.CharField(max_length=1024)
    release_group = models.CharField(max_length=32)
    is_scene = models.NullBooleanField(default=False)
    description = models.TextField()
    nfo = models.TextField()
    mediainfo = models.OneToOneField(to='mediainfo.Mediainfo', null=True)

    # Format information
    is_3d = models.BooleanField(default=False)
    is_source = models.BooleanField(default=False)
    source_media = models.ForeignKey(
        to='media_formats.SourceMedia',
        related_name='torrents',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
    )
    resolution = models.ForeignKey(
        to='media_formats.Resolution',
        related_name='torrents',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
    )
    codec = models.ForeignKey(
        to='media_formats.Codec',
        related_name='torrents',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
    )
    container = models.ForeignKey(
        to='media_formats.Container',
        related_name='torrents',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
    )

    # BitTorrent information
    swarm = models.OneToOneField('tracker.Swarm', related_name='torrent', db_index=True)
    metainfo = models.OneToOneField('torrents.TorrentMetaInfo', related_name='torrent')
    file_list = PickledObjectField(null=False)
    size_in_bytes = models.BigIntegerField(null=False)

    class Meta:
        permissions = (
            ('can_upload', "Can upload new torrents"),
            ('can_moderate', "Can moderate torrents"),
            ('can_request_reseed', "Can request a reseed"),
        )

    def __str__(self):
        return self.swarm_id

    def get_absolute_url(self):
        return reverse(
            viewname='film_torrent_details',
            kwargs={
                'film_id': self.film_id,
                'torrent_id': self.id,
            }
        )

    @property
    def format(self):
        return '{codec} / {container} / {resolution} / {source_media}'.format(
            codec=self.codec_id,
            container=self.container_id,
            resolution=self.resolution_id,
            source_media=self.source_media_id,
        )

    @property
    def is_accepting_reseed_requests(self):
        one_day_ago = now() - timedelta(days=1)
        one_week_ago = now() - timedelta(days=7)
        return all((
            self.uploaded_at < one_day_ago,
            self.last_seeded is None or self.last_seeded < one_day_ago,
            self.reseed_request is None or self.reseed_request.created_at < one_week_ago,
        ))

    def request_reseed(self, user_profile):
        self.reseed_request = self.reseed_requests.create(
            created_by=user_profile,
        )
        self.save()


class TorrentMetaInfo(models.Model):

    dictionary = PickledObjectField(null=False)

    def __str__(self):
        return str(self.torrent)

    def for_user_download(self, user_profile):

        # Make sure the private flag is set
        self.dictionary['info']['private'] = 1

        # Set the announce url
        self.dictionary['announce'] = user_profile.announce_url

        # Return the bencoded version
        return bencode(self.dictionary)


class ReseedRequest(models.Model):

    # TODO: notify the torrent's uploader and the snatch list when one of these is created

    torrent = models.ForeignKey(
        to='torrents.Torrent',
        related_name='reseed_requests',
    )
    created_by = models.ForeignKey(
        to='profiles.UserProfile',
        related_name='reseed_requests',
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    fulfilled_at = models.DateTimeField(null=True)
