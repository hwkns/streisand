# -*- coding: utf-8 -*-

from hashlib import md5, sha1

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User, Permission
from django.db.models import Q

from profiles.models import UserProfile


class CustomAuthBackend(ModelBackend):

    def get_user(self, user_id):
        try:
            profile = UserProfile.objects.filter(
                user_id=user_id
            ).select_related(
                'user',
                'user_class',
            ).get()
        except User.DoesNotExist:
            user = None
        else:
            user = profile.user
        return user

    def authenticate(self, username=None, password=None, **kwargs):
        """
        Django's built-in ModelBackend assumes usernames are case-sensitive
        during authentication, which can be non-intuitive.  This method supports
        case-insensitive username authentication.
        """

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

    def has_perm(self, user_obj, perm, obj=None):
        if not user_obj.is_active:
            return False
        return perm in self.get_all_permissions(user_obj, obj)

    def get_all_permissions(self, user, obj=None):
        """
        Returns a set of permission strings the user has from their groups,
        user class, and custom permissions.
        """
        if not user.is_active or user.is_anonymous() or obj is not None:
            return set()

        if not hasattr(user, '_perm_cache'):

            permissions = Permission.objects.filter(
                # User permissions
                Q(user=user)
                # Group permissions
                | Q(group__user=user)
                # UserClass permissions
                | Q(user_classes__user_profiles__user=user)
            ).distinct().values_list(
                'content_type__app_label',
                'codename',
            )

            user._perm_cache = set(
                '{app_label}.{codename}'.format(
                    app_label=app_label,
                    codename=codename,
                )
                for app_label, codename
                in permissions
            )

        return user._perm_cache

    @staticmethod
    def get_user_class_permissions(user):
        """
        Returns a set of permission strings the user has from their user class.
        """

        perm_cache_name = '_user_class_perm_cache'

        if not hasattr(user, perm_cache_name):

            permissions = Permission.objects.filter(
                Q(user=user)
                | Q(group__user=user)
                | Q(user_classes__user_profiles__user=user)
            ).distinct().values_list(
                'content_type__app_label',
                'codename',
            )

            permissions = set(
                '{app_label}.{codename}'.format(
                    app_label=app_label,
                    codename=codename,
                )
                for app_label, codename
                in permissions
            )

            setattr(user, perm_cache_name, permissions)

        return getattr(user, perm_cache_name)


class OldSiteAuthBackend(ModelBackend):
    """
    The old site used md5 and sha1 with a salt to store passwords.
    """

    @staticmethod
    def old_site_password_hash(string, secret):
        old_site_salt = settings.OLD_SITE_SECRET_KEY
        secret = secret.encode('utf-8')
        secret_md5 = md5(secret).hexdigest()
        secret_sha1 = sha1(secret).hexdigest()
        things = (secret_md5 + string + secret_sha1 + old_site_salt).encode('utf-8')
        return sha1(things).hexdigest()

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            # Calculate a password hash to reduce the timing difference
            # between an existing and a non-existing user.
            self.old_site_password_hash('password', 'salt')
        else:
            # User does exist; check if they have an old-style hash
            if user.password.startswith('old_hash$'):
                # Check the old hash against the provided password
                (prefix, password_hash, salt) = user.password.split('$')
                if self.old_site_password_hash(password, salt) == password_hash:
                    # Update the password hash and authenticate the user
                    user.set_password(password)
                    user.save()
                    return user
            else:
                # Calculate a password hash to reduce the timing difference
                # between an existing and a non-existing user.
                self.old_site_password_hash('password', 'salt')

        return None
