# -*- coding: utf-8 -*-

from django.db import models


class Comment(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('profiles.UserProfile', related_name='%(class)ss')
    text = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.text
