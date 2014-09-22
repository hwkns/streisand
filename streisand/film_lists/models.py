# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.db import models


class FilmList(models.Model):
    title = models.CharField(max_length=1024)
    description = models.TextField()
    films = models.ManyToManyField(to='films.Film', through='film_lists.FilmListItem')

    def __str__(self):
        return 'FilmList <{title}>'.format(title=self.title)

    def get_absolute_url(self):
        return reverse('film_list_details', args=[self.id])


class FilmListItem(models.Model):
    film = models.ForeignKey('films.Film')
    film_list = models.ForeignKey('film_lists.FilmList')
    sequence_number = models.IntegerField

    class Meta:
        unique_together = ['film_list', 'sequence_number']
