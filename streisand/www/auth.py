# -*- coding: utf-8 -*-

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from .utils import old_site_password_hash


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
            # difference between an existing and a non-existing user.
            User().set_password(password)


class OldSiteAuthBackend(ModelBackend):
    """
    The old site used md5 and sha1 with a salt to store passwords.
    """

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            # Calculate a password hash to reduce the timing difference
            # between an existing and a non-existing user.
            old_site_password_hash('password', 'salt')
        else:
            # User does exist; check if they have an old-style hash
            if user.password.startswith('old_hash$'):
                # Check the old hash against the provided password
                (prefix, password_hash, salt) = user.password.split('$')
                if old_site_password_hash(password, salt) == password_hash:
                    # Update the password hash and authenticate the user
                    user.set_password(password)
                    user.save()
                    return user
            else:
                # Calculate a password hash to reduce the timing difference
                # between an existing and a non-existing user.
                old_site_password_hash('password', 'salt')

        return None
