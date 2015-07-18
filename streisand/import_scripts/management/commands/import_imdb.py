# -*- coding: utf-8 -*-

from pytz import UTC

from import_scripts.management.commands import MySQLCommand

from imdb.models import FilmIMDb


class Command(MySQLCommand):

    SQL = """
        SELECT * FROM imdb_information
        WHERE imdbID IN (
            SELECT IMDB FROM torrents_group WHERE ID IN (
                SELECT DISTINCT GroupID FROM torrents WHERE ID < 1000
            )
        )
        OR imdbID IN (SELECT imdbID FROM requests WHERE ID < 1000)
    """

    help = "Imports IMDb information from the MySQL db"

    def handle_row(self, row):

        imdb_id = row['imdbID']
        rating = row['rating']
        rating_vote_count = row['votes']
        runtime_in_minutes = row['runtime']
        last_updated = row['updatedOn']

        i = FilmIMDb.objects.create(
            id=imdb_id,
            rating=rating,
            rating_vote_count=rating_vote_count,
            runtime_in_minutes=runtime_in_minutes,
            last_updated=last_updated.replace(tzinfo=UTC) if last_updated else None,
        )

        print(i.tt_id)
