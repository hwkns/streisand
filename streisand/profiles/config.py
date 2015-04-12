# -*- coding: utf-8 -*-

import logging

from django.apps import AppConfig


class ProfilesAppConfig(AppConfig):

    name = 'profiles'
    verbose_name = 'User Profiles'

    def ready(self):

        import profiles.signals.handlers
        logging.debug('Imported {module}'.format(module=profiles.signals.handlers))
