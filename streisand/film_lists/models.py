# -*- coding: utf-8 -*-

from django.db import models
from django.urls import reverse


class FilmList(models.Model):
    title = models.CharField(max_length=1024)
    description = models.TextField()
    films = models.ManyToManyField(
        to='films.Film',
        related_name='film_lists',
        through='film_lists.FilmListItem',
    )

    def __str__(self):
        return self.title

    def __len__(self):
        return self.films.count()

    def get_absolute_url(self):
        return reverse('film_list_details', args=[self.id])


class FilmListItem(models.Model):
    film_list = models.ForeignKey(
        to='film_lists.FilmList',
        related_name='items',
        db_index=True,
        on_delete=models.CASCADE,
    )
    film = models.ForeignKey(
        to='films.Film',
        on_delete=models.PROTECT,
    )

    class Meta:
        unique_together = ['film_list', 'film']
        order_with_respect_to = 'film_list'
