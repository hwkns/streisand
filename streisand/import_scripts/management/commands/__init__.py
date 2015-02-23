# -*- coding: utf-8 -*-

import mysql.connector

from django.core.management.base import BaseCommand


class MySQLCommand(BaseCommand):

    DB_CONFIG = {
        'user': 'root',
        'host': '10.0.2.2',
        'database': 'tc',
        'charset': 'latin1',
    }

    SQL = ""

    help = "*******************************"

    def handle(self, *args, **options):

        self.pre_sql()

        cnx = mysql.connector.connect(**self.DB_CONFIG)
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(self.SQL)
        for row in cursor:
            self.handle_row(row)
        cursor.close()
        cnx.close()

        self.post_sql()

    @staticmethod
    def pre_sql():
        pass

    @staticmethod
    def handle_row(row):
        pass

    @staticmethod
    def post_sql():
        pass
