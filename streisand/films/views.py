# -*- coding: utf-8 -*-

from django.http import Http404
from django.shortcuts import render

from .models import Film


def film_index(request):
    return render(
        request=request,
        template_name='film_index.html',
        dictionary={
            'films': Film.objects.all(),
        }
    )


def film_details(request, film_id, torrent_id=None):

    try:
        film = Film.objects.filter(id=film_id).prefetch_related('torrents').get()
    except Film.DoesNotExist:
        raise Http404

    if torrent_id is not None:
        torrent_id = int(torrent_id)

    return render(
        request=request,
        template_name='film_details.html',
        dictionary={
            'film': film,
            'torrent_id': torrent_id,
        }
    )
