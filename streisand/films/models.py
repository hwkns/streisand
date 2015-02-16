# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.db import models


class Film(models.Model):

    title = models.CharField(max_length=1024)
    year = models.PositiveSmallIntegerField()
    imdb_id = models.CharField(max_length=9)
    tmdb_id = models.IntegerField()
    poster_url = models.URLField()
    fanart_url = models.URLField()
    trailer_url = models.URLField()
    trailer_type = models.CharField(max_length=64)
    duration_in_minutes = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('film_details', args=[self.id])

    @staticmethod
    def autocomplete_search_fields():
        return (
            "title__icontains",
        )