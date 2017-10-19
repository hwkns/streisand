# -*- coding: utf-8 -*-

from import_scripts.management.commands import MySQLCommand
from profiles.models import UserProfile
from torrent_requests.models import TorrentRequest


class Command(MySQLCommand):

    SQL = """
        SELECT * FROM requests_votes
    """

    help = "Imports request votes from the MySQL db"

    def handle_row(self, row):

        request_id = row['RequestID']
        voter_id = row['UserID']

        try:
            voter = UserProfile.objects.get(old_id=voter_id)
        except UserProfile.DoesNotExist:
            return
        try:
            torrent_request = TorrentRequest.objects.get(old_id=request_id)
        except TorrentRequest.DoesNotExist:
            return

        vote = torrent_request.votes.create(
            author=voter,
            bounty_in_bytes=0,
        )

        print(vote)
