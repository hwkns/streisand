# -*- coding: utf-8 -*-

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


def film_details(request, film_id):
    film = Film.objects.filter(id=film_id).prefetch_related('torrents').get()
    return render(
        request=request,
        template_name='film_details.html',
        dictionary={
            'film': film,
        }
    )
