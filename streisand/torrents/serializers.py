# -*- coding: utf-8 -*-

from rest_framework import serializers

from django.template.defaultfilters import filesizeformat

from mediainfo.serializers import AdminMediainfoSerializer

from .models import Torrent


class AdminTorrentSerializer(serializers.ModelSerializer):

    size = serializers.SerializerMethodField()
    info_hash = serializers.CharField(source='swarm_id')
    file_list = serializers.ListField()
    mediainfo = AdminMediainfoSerializer()

    class Meta:
        model = Torrent
        fields = (
            'id',
            'film_id',
            'cut',
            'codec',
            'container',
            'resolution',
            'source_media',
            'is_source',
            'is_3d',
            'size',
            'uploaded_by',
            'uploaded_at',
            'last_seeded',
            'snatch_count',
            'reseed_request',
            'is_accepting_reseed_requests',
            'is_approved',
            'moderated_by',
            'release_name',
            'release_group',
            'is_scene',
            'info_hash',
            'file_list',
            'nfo',
            'mediainfo',
            'description',
        )

    @staticmethod
    def get_size(obj):
        return filesizeformat(obj.size_in_bytes)


class PublicTorrentSerializer(AdminTorrentSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        remove_fields = (
            'moderated_by',
        )
        for field_name in remove_fields:
            self.fields.pop(field_name)
