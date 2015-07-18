# -*- coding: utf-8 -*-

from pytz import UTC

from import_scripts.management.commands import MySQLCommand
from profiles.models import UserProfile
from torrent_requests.models import TorrentRequest


class Command(MySQLCommand):

    SQL = """
        SELECT * FROM requests_comments
        WHERE RequestID IN (SELECT ID FROM requests WHERE ID < 1000)
    """

    help = "Imports request comments from the MySQL db"

    def handle_row(self, row):

        request_id = row['RequestID']
        author_id = row['AuthorID']
        body = row['Body']
        submit_date = row['AddedTime']
        edit_date = row['EditedTime']

        try:
            author = UserProfile.objects.get(old_id=author_id)
        except UserProfile.DoesNotExist:
            return
        torrent_request = TorrentRequest.objects.get(old_id=request_id)

        comment = torrent_request.comments.create(
            author=author,
            text=body.encode('latin-1').decode('utf-8') if body else '',
        )
        comment.created_at = submit_date.replace(tzinfo=UTC)
        if edit_date:
            comment.modified_at = edit_date.replace(tzinfo=UTC)
        else:
            comment.modified_at = comment.created_at
        comment.save(update_fields=['created_at', 'modified_at'])

        print(comment)
