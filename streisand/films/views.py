# -*- coding: utf-8 -*-

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import render

from .models import Film


def film_index(request):

    all_films = Film.objects.all()
    paginator = Paginator(all_films, 50)  # Show 50 films per page

    page = request.GET.get('page')
    try:
        films = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        films = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        films = paginator.page(paginator.num_pages)

    return render(
        request=request,
        template_name='film_index.html',
        dictionary={
            'films': films,
        }
    )


def film_details(request, film_id, torrent_id=None):

    try:
        film = Film.objects.filter(id=film_id).prefetch_related('torrents', 'comments').get()
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
