# -*- coding: utf-8 -*-

from django.shortcuts import render

from .models import Torrent


def index(request):
    return render(
        request=request,
        template_name='torrents.html',
        dictionary={
            'torrents': Torrent.objects.all(),
        }
    )


def torrent_view(request, torrent_id):
    torrent = Torrent.objects.filter(id=torrent_id).select_related('swarm').get()
    return render(
        request=request,
        template_name='torrent.html',
        dictionary={
            'torrent': torrent,
        }
    )
