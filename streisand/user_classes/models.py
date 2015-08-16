# -*- coding: utf-8 -*-

from django.db import models


class UserClass(models.Model):

    old_id = models.PositiveIntegerField(null=True, db_index=True)

    name = models.CharField(primary_key=True, max_length=128)
    rank = models.PositiveSmallIntegerField(db_index=True)
    is_staff = models.BooleanField(default=False, db_index=True)
    permissions = models.ManyToManyField(
        to='auth.Permission',
        related_name='user_classes',
        blank=True,
    )

    class Meta:
        ordering = ['rank']

    def __str__(self):
        return self.name
