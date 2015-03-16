# -*- coding: utf-8 -*-

from import_scripts.management.commands import MySQLCommand
from tracker.models import TorrentClient


class Command(MySQLCommand):

    SQL = """SELECT * FROM xbt_client_whitelist ORDER BY peer_id"""

    help = "Imports whitelisted client info from the MySQL db"

    def handle_row(self, row):

        peer_id_prefix = row['peer_id']
        name = row['vstring'].encode('latin-1').decode('utf-8')
        c = TorrentClient.objects.create(
            peer_id_prefix=peer_id_prefix,
            name=name,
            whitelisted=True,
        )

        print(c)
