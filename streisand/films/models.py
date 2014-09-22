# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.db import models


class Film(models.Model):
    title = models.CharField(max_length=1024)
    imdb_id = models.CharField(max_length=9)
    tmdb_id = models.IntegerField()
    poster_url = models.URLField()
    fanart_url = models.URLField()
    trailer_type = models.CharField(max_length=64)
    trailer_url = models.URLField()
    duration_in_minutes = models.IntegerField()
    description = models.TextField()

    def get_absolute_url(self):
        return reverse('film_details', args=[self.id])
