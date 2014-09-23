# -*- coding: utf-8 -*-

from django_dynamic_fixture import G

from django.test import TestCase

from torrents.models import Torrent

from profiles.models import UserProfile, TorrentStats
from profiles.tasks import handle_announce


class TorrentStatsTests(TestCase):

    def setUp(self):
        self.profile = G(UserProfile)
        self.torrent = G(Torrent)

    def upload(self, amount):
        handle_announce(
            auth_key=self.profile.auth_key_id,
            info_hash=self.torrent.info_hash,
            peer_id='baz',
            ip_address='0.0.0.0',
            port='1234',
            user_agent='',
            new_bytes_uploaded=amount,
            new_bytes_downloaded=0,
            bytes_remaining=0,
            event='',
            time_stamp=0.0,
        )

    def test_announce_handler_tracks_uploaded_data(self):
        self.upload(100)
        stats = TorrentStats.objects.get(profile=self.profile, torrent=self.torrent)
        self.assertEqual(stats.bytes_uploaded, 100)
        self.upload(100)
        stats = TorrentStats.objects.get(profile=self.profile, torrent=self.torrent)
        self.assertEqual(stats.bytes_uploaded, 200)
