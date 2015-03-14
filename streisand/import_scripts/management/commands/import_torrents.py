# -*- coding: utf-8 -*-

import os
from binascii import b2a_hex

from pytz import UTC

from django.conf import settings

from import_scripts.management.commands import MySQLCommand
from films.models import Film
from profiles.models import UserProfile
from torrents.models import Torrent, TorrentMetaInfo
from tracker.models import Swarm
from tracker.bencoding import bdecode


class Command(MySQLCommand):

    SQL = """SELECT * FROM torrents WHERE ID < 1000"""

    help = "Imports torrents from files and the MySQL db"

    torrent_ids = set()

    def handle_row(self, row):

        torrent_id = row['ID']
        torrent_group_id = row['GroupID']
        info_hash = b2a_hex(row['info_hash']).decode('utf-8')
        uploader_id = row['UserID']
        uploaded_at = row['Time']
        source_media = row['media']
        resolution = row['Encoding']
        codec = row['Format']
        container = row['container']
        is_special_edition = (row['Remastered'] == '1')
        special_edition_title = row['RemasterTitle']
        # special_edition_year = row['Year']
        is_scene = (row['Scene'] == '1')
        # scene_title = row['SceneTitle']
        bbcode_description = row['Description']
        nfo_text = row['nfo']
        release_name = row['ReleaseName']
        size_in_bytes = row['Size']
        # last_action = row['last_action']
        # imdb_id = row['imdb']
        # is_moderated = (row['Moderated'] == 1)
        # last_moderated_by_username = row['LastModeratedBy']
        # tc_original = (row['Exclusive'] == '1')
        # reseed_requested_at = row['ReseedRequested']
        mediainfo = row['MediaInfo']

        metainfo_dict = self.get_metainfo(torrent_id)
        if 'files' in metainfo_dict['info']:
            file_list = [
                '/'.join(file['path'])
                for file
                in metainfo_dict['info']['files']
            ]
        else:
            file_list = [
                metainfo_dict['info']['name']
            ]

        swarm = Swarm.objects.create(torrent_info_hash=info_hash)
        metainfo = TorrentMetaInfo.objects.create(dictionary=metainfo_dict)
        uploader = UserProfile.objects.filter(old_id=uploader_id).first()

        torrent = Torrent.objects.create(
            old_id=torrent_id,
            film=Film.objects.get(old_id=torrent_group_id),
            cut=special_edition_title if is_special_edition else 'Theatrical',
            description=bbcode_description.encode('latin-1').decode('utf-8') if bbcode_description else '',
            nfo=nfo_text.encode('latin-1').decode('utf-8') if nfo_text else '',
            mediainfo=mediainfo.encode('latin-1').decode('utf-8') if mediainfo else '',
            swarm=swarm,
            metainfo=metainfo,
            file_list=file_list,
            uploaded_at=uploaded_at.replace(tzinfo=UTC),
            uploaded_by=uploader,
            source_media_id=source_media,
            resolution_id=resolution,
            codec_id=codec,
            container_id=container,
            release_name=release_name.encode('latin-1').decode('utf-8') if release_name else '',
            is_scene=is_scene,
            size_in_bytes=size_in_bytes,
        )

        print(torrent)

    @staticmethod
    def get_metainfo(torrent_id):
        path = os.path.join(settings.BASE_DIR, '../torrents/{torrent_id}.torrent'.format(torrent_id=torrent_id))
        with open(path, 'rb') as f:
            torrent_bytes = f.read()
        return bdecode(torrent_bytes)
