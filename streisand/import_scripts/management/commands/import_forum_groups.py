# -*- coding: utf-8 -*-

from import_scripts.management.commands import MySQLCommand

from forums.models import ForumGroup


class Command(MySQLCommand):

    SQL = """
        SELECT * FROM forums_groups ORDER BY Sort
    """

    help = "Imports forum groups from the MySQL db"

    def handle_row(self, row):

        old_id = row['ID']
        sort = row['Sort']
        name = row['Name']

        forum_group = ForumGroup.objects.create(
            old_id=old_id,
            sort_order=sort,
            name=name,
        )

        print(forum_group)
