# -*- coding: utf-8 -*-

from django.db import models


class Codec(models.Model):

    name = models.CharField(max_length=64)

    def __str__(self):
        return '{name}'.format(name=self.name)


class Container(models.Model):

    name = models.CharField(max_length=64)

    def __str__(self):
        return '{name}'.format(name=self.name)


class Resolution(models.Model):

    name = models.CharField(max_length=64)

    def __str__(self):
        return '{name}'.format(name=self.name)


class SourceMedia(models.Model):

    name = models.CharField(max_length=64)

    def __str__(self):
        return '{name}'.format(name=self.name)
