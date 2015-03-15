# -*- coding: utf-8 -*-

from pytz import UTC

from django.conf import settings

from django_comments.models import Comment

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

        try:
            author = UserProfile.objects.get(old_id=author_id)
        except UserProfile.DoesNotExist:
            return
        film = Film.objects.get(old_id=torrent_group_id)

        comment = Comment.objects.create(
            site_id=settings.SITE_ID,
            content_object=film,
            user_name=author.username,
            user=author.user,
            comment=body,
            submit_date=submit_date.replace(tzinfo=UTC),
        )

        print(comment)
