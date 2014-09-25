# -*- coding: utf-8 -*-

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class CaseInsensitiveAuthBackend(ModelBackend):
    """
    Django's built-in ModelBackend assumes usernames are case-sensitive
    during authentication, which can be non-intuitive.  This backend supports
    case-insensitive username authentication.
    """

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username__iexact=username)
            if user.check_password(password):
                return user
            else:
                return None
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            User().set_password(password)
