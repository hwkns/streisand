# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import SESSION_KEY, get_user
from django.contrib.auth.models import User, AnonymousUser
from django.core.cache import cache
from django.db.models import signals
from django.utils.functional import SimpleLazyObject
from django.utils.http import urlquote

from profiles.models import UserProfile


class LoginRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of prefixes in settings.LOGIN_EXEMPT_URL_PREFIXES.

    Inspired by:
    http://onecreativeblog.com/post/59051248/django-login-required-middleware
    """

    LOGIN_EXEMPT_URL_PREFIXES = (
        settings.LOGIN_URL,
    )
    if hasattr(settings, 'LOGIN_EXEMPT_URL_PREFIXES'):
        LOGIN_EXEMPT_URL_PREFIXES += tuple(settings.LOGIN_EXEMPT_URL_PREFIXES)

    def process_request(self, request):
        if not request.user.is_authenticated():
            if not request.path_info.startswith(self.LOGIN_EXEMPT_URL_PREFIXES):
                redirect_path = '{login_url}?next={next_url}'.format(
                    login_url = settings.LOGIN_URL,
                    next_url = urlquote(request.get_full_path()),
                )
                return HttpResponseRedirect(redirect_path)


class CachedUserAuthenticationMiddleware(object):
    """
    Middleware that caches request.user for a session so it doesn't have to be
    looked up in the database for every page load.

    Inspired by: https://github.com/ui/django-cached_authentication_middleware
    """

    CACHE_KEY = 'cached_user_authentication_middleware:{user_id}'

    def __init__(self):
        signals.post_save.connect(self.invalidate_user_cache, sender=User)
        signals.post_save.connect(self.invalidate_user_cache, sender=UserProfile)
        signals.post_delete.connect(self.invalidate_user_cache, sender=User)
        signals.post_delete.connect(self.invalidate_user_cache, sender=UserProfile)

    def process_request(self, request):
        request.user = SimpleLazyObject(
            lambda: self.get_cached_user_from_request(request)
        )

    def invalidate_user_cache(self, sender, instance, **kwargs):
        if isinstance(instance, User):
            key = self.CACHE_KEY.format(user_id=instance.id)
        else:
            key = self.CACHE_KEY.format(user_id=instance.user_id)
        cache.delete(key)

    def get_cached_user_from_request(self, request):

        if not hasattr(request, '_cached_user'):

            try:

                key = self.CACHE_KEY.format(
                    user_id=request.session[SESSION_KEY]
                )

            except KeyError:

                request._cached_user = AnonymousUser()

            else:

                # Try to get the cached user object
                user = cache.get(key)

                # On a cache miss, get the user and cache it
                if user is None:
                    user = get_user(request)
                    if hasattr(user, 'profile'):
                        user.profile
                    cache.set(key, user)

                request._cached_user = user

        return request._cached_user
