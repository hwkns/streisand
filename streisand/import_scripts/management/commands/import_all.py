# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):

    help = "Import all data from the old site db"

    def handle(self, *args, **options):
        call_command('import_tags')
        call_command('import_films')
        call_command('import_users')
        call_command('import_torrents')
