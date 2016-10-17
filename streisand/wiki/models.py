# -*- coding: utf-8 -*-

from django.db import models
from django.urls import reverse


class WikiPage(models.Model):

    old_id = models.PositiveIntegerField(null=True, db_index=True)

    author = models.ForeignKey(
        to='profiles.UserProfile',
        related_name='wiki_pages',
        null=True,  # TODO: turn this off
    )
    slug = models.SlugField(unique=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = 'created_at'

    def __str__(self):
        return 'Wiki page by {author}'.format(
            author=self.author,
        )

    def get_absolute_url(self):
        return reverse('wiki_page', args=[self.slug])
