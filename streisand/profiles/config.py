# -*- coding: utf-8 -*-

from django.apps import AppConfig


class ProfilesAppConfig(AppConfig):

    name = 'profiles'
    verbose_name = 'User Profiles'

    def ready(self):

        # noinspection PyUnresolvedReferences
        import profiles.signals.handlers  # NOQA
