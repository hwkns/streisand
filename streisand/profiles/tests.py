# -*- coding: utf-8 -*-

from django_dynamic_fixture import G

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.timezone import now

from torrents.models import Torrent
from torrent_stats.models import TorrentStats

from .tasks import handle_announce


class TorrentAnnounceTests(TestCase):

    def setUp(self):
        self.user = G(User)
        self.profile = self.user.profile
        self.torrent = G(Torrent, uploaded_by=self.profile)

    def upload(self, amount):
        handle_announce(
            announce_key=self.profile.announce_key_id,
            torrent_info_hash=self.torrent.swarm_id,
            peer_id='baz',
            ip_address='0.0.0.0',
            port='1234',
            user_agent='',
            new_bytes_uploaded=amount,
            new_bytes_downloaded=0,
            bytes_remaining=0,
            event='',
            time_stamp=now(),
        )

    def test_announce_handler_tracks_uploaded_data(self):
        self.upload(100)
        stats = TorrentStats.objects.get(profile=self.profile, torrent=self.torrent)
        self.assertEqual(stats.bytes_uploaded, 100)
        self.upload(100)
        stats = TorrentStats.objects.get(profile=self.profile, torrent=self.torrent)
        self.assertEqual(stats.bytes_uploaded, 200)

    def test_successful_announce_is_logged(self):
        self.profile.log_successful_announces = True
        self.profile.save()
        self.upload(100)
        log = self.profile.logged_announces.get()
        self.assertEqual(log.announce_key, self.profile.announce_key_id)
        self.assertEqual(log.swarm_id, self.torrent.swarm_id)
        self.assertEqual(log.new_bytes_uploaded, 100)
        self.assertEqual(log.new_bytes_downloaded, 0)
        self.assertEqual(log.bytes_remaining, 0)
