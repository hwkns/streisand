# -*- coding: utf-8 -*-

import logging
from hashlib import md5, sha1
from urllib.parse import urljoin

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def get_full_url(relative_url):
    return urljoin(settings.SITE_URL, relative_url)


def email(subject='', template='', context=None, from_email=None, reply_to=None, to=(), cc=(), bcc=()):

    if from_email is None:
        from_email = '{name} <{email}>'.format(
            name=settings.SITE_NAME,
            email=settings.DEFAULT_FROM_EMAIL,
        )

    if reply_to is None:
        reply_to = settings.DEFAULT_REPLY_TO_EMAIL

    html = render_to_string(template, context)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=strip_tags(html),
        from_email=from_email,
        to=to,
        cc=cc,
        bcc=bcc,
        headers={
            'Reply-To': reply_to
        },
    )
    msg.attach_alternative(html, 'text/html')

    try:
        msg.send()
    except Exception:
        logging.exception('Failed to send email "{subject}" to {recipients}'.format(
            subject=subject,
            recipients=to,
        ))


def old_site_password_hash(string, secret):
    old_site_salt = settings.OLD_SITE_HASH
    secret = secret.encode('utf-8')
    secret_md5 = md5(secret).hexdigest()
    secret_sha1 = sha1(secret).hexdigest()
    things = (secret_md5 + string + secret_sha1 + old_site_salt).encode('utf-8')
    return sha1(things).hexdigest()
