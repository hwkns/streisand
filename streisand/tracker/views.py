# -*- coding: utf-8 -*-

from urllib.parse import unquote_to_bytes
import pprint

from django.views.generic import View
from django.http import HttpResponse, HttpResponseNotFound
from django.core.cache import cache

from .bencoding import bencode


cache.set(
    '16fd2706-8baf-433b-82eb-8c7fada847da',
    'hwkns'
)

PEER_ID_WHITELIST = {
    b'-UT3400-000000000000',
}

TORRENTS = {
    b'\x89I\x85\xf9|\xc2\\$n7\xa0|\xd7\xc7\x85\x999\x82\xa7\xcb': 'pr0n',
}


class AnnounceView(View):

    def get(self, request, auth_key):

        params = dict(
            [param.split('=') for param in request.META['QUERY_STRING'].split('&')]
        )

        info_hash = unquote_to_bytes(params.get('info_hash', b''))
        peer_id = unquote_to_bytes(params.get('peer_id', b''))
        port = request.GET.get('port')
        uploaded = request.GET.get('uploaded')
        downloaded = request.GET.get('downloaded')
        left = request.GET.get('left')
        compact = request.GET.get('compact', '1')
        event = request.GET.get('event')
        numwant = request.GET.get('numwant', '50')
        key = request.GET.get('key')
        ip = request.META['REMOTE_ADDR']

        # Parameters we don't care about:
        #
        #    no_peer_id - We always send compact responses
        #
        #    ip - No proxy announcing allowed; we will distribute
        #        the IP from which this request originated
        #
        #    trackerid - Most clients don't implement this, and we
        #        have no use for it

        print(params)
        # print(cache.keys('*'))

        if not cache.get(auth_key):
            return HttpResponse(bencode({
                'failure reason': 'Invalid auth key'
            }))
        elif peer_id not in PEER_ID_WHITELIST:
            return HttpResponse(bencode({
                'failure reason': 'Your client is not in the whitelist'
            }))
        elif compact == '0':
            return HttpResponse(bencode({
                'failure reason': 'This tracker only sends compact responses'
            }))
        elif info_hash not in TORRENTS:
            return HttpResponse(bencode({
                'failure reason': 'Unregistered torrent'
            }))

        return HttpResponse(
            'Auth key: {auth_key}<br/>'
            'User: {user}<br/>'
            'IP: {ip}<br/>'
            'Torrent: {torrent}<br/>'
            '<br/>Params: <pre>{params}</pre><br/>'.format(
                auth_key=auth_key,
                user=cache.get(auth_key),
                ip=ip,
                params=pprint.pformat(params),
                torrent=TORRENTS.get(info_hash),
            )
        )
