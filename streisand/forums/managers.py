# -*- coding: utf-8 -*-

from django.db import models


class ForumTopicManager(models.Manager):

    def accessible_to_user(self, user):
        return self.exclude(minimum_user_class__rank__gt=user.profile.user_class.rank)


class ForumThreadManager(models.Manager):

    def accessible_to_user(self, user):
        return self.exclude(topic__minimum_user_class__rank__gt=user.profile.user_class.rank)
