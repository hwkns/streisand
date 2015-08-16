# -*- coding: utf-8 -*-

from pytz import UTC

from django.utils.timezone import datetime, timedelta

from import_scripts.management.commands import MySQLCommand
from profiles.models import UserProfile
from torrents.models import Torrent
from torrent_stats.models import TorrentStats


class Command(MySQLCommand):

    SQL = """SELECT * FROM xbt_snatched WHERE fid < 1000 ORDER BY tstamp"""

    help = "Imports torrent snatches from the MySQL db"

    def handle_row(self, row):

        torrent_id = row['fid']
        user_id = row['uid']
        timestamp = datetime.fromtimestamp(row['tstamp'], UTC)
        seed_time_in_seconds = row['seedtime']

        try:
            profile = UserProfile.objects.get(old_id=user_id)
            torrent = Torrent.objects.get(old_id=torrent_id)
        except (UserProfile.DoesNotExist, Torrent.DoesNotExist):
            return

        torrent_stats, created = TorrentStats.objects.get_or_create(
            profile=profile,
            torrent=torrent,
        )
        torrent_stats.snatch_count += 1
        torrent_stats.last_snatched = timestamp
        if torrent_stats.first_snatched is None:
            torrent_stats.first_snatched = timestamp
        torrent_stats.seed_time = timedelta(seconds=seed_time_in_seconds)
        torrent_stats.save()

        print(torrent_stats)
