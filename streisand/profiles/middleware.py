# -*- coding: utf-8 -*-

from django.utils.deprecation import MiddlewareMixin

from profiles.models import UserIPAddress


class IPHistoryMiddleware(MiddlewareMixin):

    @staticmethod
    def process_request(request):
        if request.user.is_authenticated:
            # Update the profile's IP history
            UserIPAddress.objects.update_or_create(
                profile=request.user.profile,
                ip_address=request.META['REMOTE_ADDR'],
                used_with='site',
            )
