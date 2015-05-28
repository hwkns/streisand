# -*- coding: utf-8 -*-

import os
import re
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

    moderation_values = {
        0: None,
        1: True,
        2: False,
    }

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
        release_name = row['ReleaseName']
        size_in_bytes = row['Size']
        # last_action = row['last_action']
        # imdb_id = row['imdb']
        is_approved = self.moderation_values[row['Moderated']]
        last_moderated_by_username = row['LastModeratedBy']
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

        nfo_text = ''
        if bbcode_description:
            description = bbcode_description.encode('latin-1').decode('utf-8').strip()
            nfo_match = re.search(
                r'\[spoiler=NFO\]\s*(?:\[size=\d\])?\s*\[pre\](.*)\[/pre\]\s*(?:\[/size\])?\s*\[/spoiler\]',
                string=description,
                flags=re.IGNORECASE + re.DOTALL,
            )
            if nfo_match:
                nfo_text = nfo_match.group(1).rstrip()
                if 'Ü' in nfo_text:
                    nfo_text = nfo_text.encode('cp1252').decode('cp437')
                spoiler_match = re.search(
                    r'(\[spoiler=NFO\]\s*(?:\[size=\d\])?\s*\[pre\].*\[/pre\]\s*(?:\[/size\])?\s*\[/spoiler\])',
                    string=description,
                    flags=re.IGNORECASE + re.DOTALL,
                )
                description = description.replace(spoiler_match.group(1), '')
        else:
            description = ''

        swarm = Swarm.objects.create(torrent_info_hash=info_hash)
        metainfo = TorrentMetaInfo.objects.create(dictionary=metainfo_dict)
        uploader = UserProfile.objects.filter(old_id=uploader_id).first()
        moderator = UserProfile.objects.filter(user__username=last_moderated_by_username).first()

        torrent = Torrent.objects.create(
            old_id=torrent_id,
            film=Film.objects.get(old_id=torrent_group_id),
            cut=special_edition_title if is_special_edition else 'Theatrical',
            description=description,
            nfo=nfo_text,
            mediainfo=mediainfo.encode('latin-1').decode('utf-8') if mediainfo else '',
            swarm=swarm,
            metainfo=metainfo,
            file_list=file_list,
            uploaded_by=uploader,
            source_media_id=source_media,
            resolution_id=resolution,
            codec_id=codec,
            container_id=container,
            release_name=release_name.encode('latin-1').decode('utf-8') if release_name else '',
            is_scene=is_scene,
            size_in_bytes=size_in_bytes,
            approved=is_approved,
            moderated_by=moderator,
        )
        torrent.uploaded_at = uploaded_at.replace(tzinfo=UTC)
        torrent.save()

        print(torrent)

    @staticmethod
    def get_metainfo(torrent_id):
        path = os.path.join(settings.BASE_DIR, '../torrents/{torrent_id}.torrent'.format(torrent_id=torrent_id))
        with open(path, 'rb') as f:
            torrent_bytes = f.read()
        return bdecode(torrent_bytes)
