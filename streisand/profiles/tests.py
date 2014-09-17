# -*- coding: utf-8 -*-

from django_dynamic_fixture import G

from django.test import TestCase

from torrents.models import Torrent

from profiles.models import UserProfile, TorrentStats
from profiles.tasks import handle_announce


class TorrentStatsTests(TestCase):

    def setUp(self):
        self.profile = G(UserProfile, auth_key='foo')
        self.torrent = G(Torrent, info_hash='bar')

    def upload(self, amount):
        handle_announce(
            auth_key='foo',
            info_hash='bar',
            peer_id='baz',
            ip_address='0.0.0.0',
            port='1234',
            new_bytes_uploaded=amount,
            new_bytes_downloaded=0,
            event=None,
        )

    def test_announce_handler_tracks_uploaded_data(self):
        self.upload(100)
        stats = TorrentStats.objects.get(profile=self.profile, torrent=self.torrent)
        self.assertEqual(stats.bytes_uploaded, 100)
        self.upload(100)
        stats = TorrentStats.objects.get(profile=self.profile, torrent=self.torrent)
        self.assertEqual(stats.bytes_uploaded, 200)
