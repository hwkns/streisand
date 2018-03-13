# -*- coding: utf-8 -*-

from django.shortcuts import render
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from www.utils import paginate
from .models import FilmList
from .serializers import FilmListSerializer


class FilmListViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FilmListSerializer
    queryset = FilmList.objects.all().prefetch_related('films__torrents')
    filter_backends = (filters.SearchFilter,)
    search_fields = ('films__title', 'title')


def film_list_index(request):

    film_lists = paginate(
        request=request,
        queryset=FilmList.objects.all(),
    )

    return render(
        request=request,
        template_name='film_list_index.html',
        context={
            'film_lists': film_lists,
        }
    )


def film_list_details(request, film_list_id):
    film_list = FilmList.objects.filter(id=film_list_id).prefetch_related('films__torrents').get()
    return render(
        request=request,
        template_name='film_list_details.html',
        context={
            'film_list': film_list,
        }
    )
