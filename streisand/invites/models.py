# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.db import models

from django_extensions.db.fields import UUIDField

from .managers import InviteManager


class Invite(models.Model):

    owner = models.ForeignKey('profiles.UserProfile', related_name='invites')
    key = UUIDField(auto=True, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = InviteManager()

    def __str__(self):
        return self.key

    def get_absolute_url(self):
        return reverse('invite_registration', kwargs={'invite_key': self.key})
