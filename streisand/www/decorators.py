# -*- coding: utf-8 -*-

from functools import wraps

from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.utils.decorators import available_attrs


def https_required(view_func):
    """
    Decorator for views that checks that the request uses SSL/TLS,
    redirecting to the HTTPS version if necessary.
    """

    @wraps(view_func, assigned=available_attrs(view_func))
    def _wrapped_view(request, *args, **kwargs):
        if not any([settings.DEBUG, request.is_secure()]):
            url = request.build_absolute_uri(request.get_full_path())
            secure_url = url.replace('http://', 'https://')
            return HttpResponsePermanentRedirect(secure_url)
        else:
            return view_func(request, *args, **kwargs)
    return _wrapped_view
