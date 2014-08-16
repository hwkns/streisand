# -*- coding: utf-8 -*-

from django.views.generic import View
from django.http import HttpResponse, HttpResponseNotFound


class AnnounceView(View):

    VALID_KEYS = {
        'qqqqqqqqqqqqqqqq',
        'zzzzzzzzzzzzzzzz',
    }

    def get(self, request, auth_key):

        if auth_key not in self.VALID_KEYS:
            return HttpResponseNotFound

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
            '{params}'.format(
                auth_key=auth_key,
                params=request.GET.dict(),
            )
        )
