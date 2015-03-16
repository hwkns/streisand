# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.db import models


class Film(models.Model):

    old_id = models.PositiveIntegerField(null=True, db_index=True)

    title = models.CharField(max_length=1024)
    year = models.PositiveSmallIntegerField(null=False)
    imdb = models.ForeignKey('imdb.FilmIMDb', null=True)
    tmdb_id = models.IntegerField(null=True, unique=True)
    poster_url = models.URLField()
    fanart_url = models.URLField()
    trailer_url = models.URLField()
    trailer_type = models.CharField(max_length=64)
    duration_in_minutes = models.IntegerField(null=True)
    description = models.TextField()
    moderation_notes = models.TextField()
    tags = models.ManyToManyField('films.Tag', related_name='films')

    def __str__(self):
        return '{title} ({year})'.format(title=self.title, year=self.year)

    def get_absolute_url(self):
        return reverse('film_details', args=[self.id])

    @staticmethod
    def autocomplete_search_fields():
        return (
            "title__icontains",
        )


class Tag(models.Model):

    name = models.CharField(max_length=32, primary_key=True)

    def __str__(self):
        return self.name
