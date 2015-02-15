# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import Torrent


class TorrentAdmin(admin.ModelAdmin):

    list_display = (
        'info_hash',
        'film',
        'codec',
        'container',
        'resolution',
        'source_media',
        'size_in_bytes',
    )

    readonly_fields = (
        'info_hash',
        'file_list',
        'last_seeded',
        'uploaded_by',
    )

    exclude = (
        'swarm',
    )

    def get_queryset(self, request):
        queryset = super(TorrentAdmin, self).get_queryset(request)
        return queryset.select_related('film')

admin.site.register(Torrent, TorrentAdmin)
