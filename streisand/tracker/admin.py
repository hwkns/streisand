# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import TorrentClient


class TorrentClientAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'peer_id_prefix',
        'whitelisted',
    )
    list_filter = (
        'whitelisted',
    )


admin.site.register(TorrentClient, TorrentClientAdmin)
