# -*- coding: utf-8 -*-

from django.shortcuts import render

from .models import FilmList


def film_list_index(request):
    return render(
        request=request,
        template_name='film_list_index.html',
        dictionary={
            'film_lists': FilmList.objects.all(),
        }
    )


def film_list_details(request, film_list_id):
    film_list = FilmList.objects.filter(id=film_list_id).prefetch_related('films__torrents').get()
    return render(
        request=request,
        template_name='film_list_details.html',
        dictionary={
            'film_list': film_list,
        }
    )
