# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.db import models

from picklefield import PickledObjectField


class Torrent(models.Model):
    swarm = models.OneToOneField('tracker.Swarm', related_name='torrent')
    film = models.ForeignKey('films.Film', null=False, db_index=True, related_name='torrents')
    uploaded_by = models.ForeignKey('profiles.UserProfile', null=False, related_name='uploaded_torrents')
    encoded_by = models.ForeignKey('profiles.UserProfile', null=True, blank=True, related_name='encodes')
    info_hash = models.CharField(max_length=40, db_index=True)
    size_in_bytes = models.BigIntegerField(null=False)
    file_list = PickledObjectField(null=False)
    last_seeded = models.DateTimeField(null=True)
    snatch_count = models.IntegerField(default=0)

    def __str__(self):
        return self.info_hash

    def __repr__(self):
        return self.__str__()

    def get_absolute_url(self):
        return reverse(
            'torrent_details',
            kwargs={
                'film_id': self.film_id,
                'torrent_id': self.id,
            }
        )
