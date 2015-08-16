# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Torrent


class TorrentAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'swarm',
        'film',
        'codec',
        'container',
        'resolution',
        'source_media',
        'size_in_bytes',
    )

    readonly_fields = (
        'swarm',
        'file_list',
        'last_seeded',
        'uploaded_by',
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'swarm',
            'film',
            'codec',
            'container',
            'resolution',
            'source_media',
        )

admin.site.register(Torrent, TorrentAdmin)
