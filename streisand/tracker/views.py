# -*- coding: utf-8 -*-

from django.views.generic import View
from django.http import HttpResponse, HttpResponseNotFound
from django.core.cache import cache

from .cache import make_auth_key
from streisand.streisand.settings import KEY_PREFIX

class AnnounceView(View):

    def get(self, request, auth_key):

        key = make_auth_key(auth_key, KEY_PREFIX)
        print(key)
        # if not cache.get(key):
        #     return HttpResponseNotFound
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
