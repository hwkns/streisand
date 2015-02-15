# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404

from .models import TorrentRequest


def torrent_request_index(request):
    return render(
        request=request,
        template_name='torrent_request_index.html',
        dictionary={
            'torrent_requests': TorrentRequest.objects.all(),
        }
    )


def torrent_request_details(request, torrent_request_id):

    torrent_request = get_object_or_404(
        TorrentRequest.objects.select_related('film'),
        id=torrent_request_id,
    )

    return render(
        request=request,
        template_name='torrent_request_details.html',
        dictionary={
            'torrent_request': torrent_request,
        }
    )
