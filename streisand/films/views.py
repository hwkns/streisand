# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404

from www.utils import paginate

from .models import Film


def film_index(request):

    films = paginate(
        request=request,
        queryset=Film.objects.all(),
    )

    return render(
        request=request,
        template_name='film_index.html',
        dictionary={
            'films': films,
        }
    )


def film_details(request, film_id, torrent_id=None):

    film = get_object_or_404(Film, id=film_id)

    if torrent_id is not None:
        torrent_id = int(torrent_id)

    torrents = film.torrents.select_related('moderated_by__user', 'uploaded_by__user')
    comments = film.comments.select_related('author__user')

    return render(
        request=request,
        template_name='film_details.html',
        dictionary={
            'film': film,
            'torrent_id': torrent_id,
            'torrents': torrents,
            'comments': comments,
        }
    )
