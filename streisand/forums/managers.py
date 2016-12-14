# -*- coding: utf-8 -*-

from django.db import models


class ForumTopicQuerySet(models.QuerySet):

    def accessible_to_user(self, user):
        if user.is_superuser:
            return self.all()
        else:
            return self.filter(minimum_user_class__rank__lte=user.profile.user_class.rank)


class ForumThreadQuerySet(models.QuerySet):

    def accessible_to_user(self, user):
        if user.is_superuser:
            return self.all()
        else:
            return self.filter(topic__minimum_user_class__rank__lte=user.profile.user_class.rank)
