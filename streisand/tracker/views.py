# -*- coding: utf-8 -*-

from django.views.generic import View
from django.http import HttpResponse, HttpResponseNotFound
from django.core.cache import cache

class AnnounceView(View):

    VALID_KEYS = {
        'auth_key:1': 'qqqqqqqqqqqqqqqq',
        'auth_ley:1 ': 'zzzzzzzzzzzzzzzz',
    }

    def get(self, request, auth_key):

        # if auth_key not in self.VALID_KEYS:
        #     return HttpResponseNotFound
        print(cache.keys('*'))
        # GET params to look for:
        #   info_hash
        #   peer_id
        #   port
        #   uploaded
        #   downloaded
        #   left
        #   compact
        #   no_peer_id
        #   event
        #   ip
        #   numwant
        #   key
        #   trackerid

        return HttpResponse(
            'Hello, world!\n\n'
            '{auth_key}\n\n'
            '{params}\n\n'
            '{redis_value}'.format(
                auth_key=auth_key,
                params=request.GET.dict(),
                redis_value=cache.get('auth_key:1'),
            )
        )
