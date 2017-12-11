# -*- coding: utf-8 -*-

import MySQLdb
from MySQLdb.cursors import SSDictCursor

from django.core.management.base import BaseCommand


class MySQLCommand(BaseCommand):

    DB_CONFIG = {
        'user': 'root',
        'password': 'fuckneebs',
        'host': '10.0.2.2',
        'db': 'tc',
        'cursorclass': SSDictCursor,
        'charset': 'latin1',
    }

    SQL = ""

    help = "*******************************"

    def handle(self, *args, **options):

        self.pre_sql()

        cnx = MySQLdb.connect(**self.DB_CONFIG)
        cursor = cnx.cursor()
        cursor.execute(self.SQL)
        for row in cursor.fetchall():
            self.handle_row(row)
        cursor.close()
        cnx.close()

        self.post_sql()

    def pre_sql(self):
        pass

    def handle_row(self, row):
        pass

    def post_sql(self):
        pass
