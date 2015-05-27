# -*- coding: utf-8 -*-

from pytz import UTC

from films.models import FilmComment

from import_scripts.management.commands import MySQLCommand
from films.models import Film
from profiles.models import UserProfile


class Command(MySQLCommand):

    SQL = """
        SELECT * FROM torrents_comments
        WHERE GroupID IN (SELECT GroupID FROM torrents WHERE ID < 1000)
    """

    help = "Imports film comments from the MySQL db"

    torrent_ids = set()

    def handle_row(self, row):

        torrent_group_id = row['GroupID']
        author_id = row['AuthorID']
        body = row['Body']
        submit_date = row['AddedTime']
        edit_date = row['EditedTime']

        try:
            author = UserProfile.objects.get(old_id=author_id)
        except UserProfile.DoesNotExist:
            return
        film = Film.objects.get(old_id=torrent_group_id)

        comment = FilmComment.objects.create(
            film=film,
            author=author,
            text=body,
        )
        comment.created_at = submit_date.replace(tzinfo=UTC)
        if edit_date:
            comment.modified_at = edit_date.replace(tzinfo=UTC)
        comment.save()

        print(comment)
