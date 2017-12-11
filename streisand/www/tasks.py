# -*- coding: utf-8 -*-

from celery import shared_task

from .utils import email


@shared_task
def async_email(*args, **kwargs):
    """
    Email wrapper for Celery
    """
    email(*args, **kwargs)
