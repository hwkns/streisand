# -*- coding: utf-8 -*-

from django_dynamic_fixture import G

from django.contrib.auth.models import User
from django.test import TestCase

from torrents.models import Torrent

from .models import TorrentStats
from .tasks import handle_announce


class TorrentAnnounceTests(TestCase):

    def setUp(self):
        self.user = G(User)
        self.profile = self.user.profile
        self.torrent = G(Torrent, uploaded_by=self.profile)

    def upload(self, amount):
        handle_announce(
            auth_key=self.profile.auth_key_id,
            swarm=self.torrent.swarm,
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

    def test_successful_announce_is_logged(self):
        self.profile.log_successful_announces = True
        self.profile.save()
        self.upload(100)
        log = self.profile.logged_announces.get()
        self.assertEqual(log.auth_key, self.profile.auth_key_id)
        self.assertEqual(log.swarm_id, self.torrent.swarm_id)
        self.assertEqual(log.new_bytes_uploaded, 100)
        self.assertEqual(log.new_bytes_downloaded, 0)
        self.assertEqual(log.bytes_remaining, 0)
