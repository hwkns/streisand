# -*- coding: utf-8 -*-

from urllib.parse import unquote_to_bytes
import pprint

from django.views.generic import View
from django.http import HttpResponse
from django.core.cache import cache

from .bencoding import bencode


cache.set(
    '16fd2706-8baf-433b-82eb-8c7fada847da',
    'hwkns'
)

ANNOUNCE_INTERVAL_IN_SECONDS = 60 * 40

PEER_ID_WHITELIST = (
    b'-AZ25',
    b'-BG10',
    b'-KT22',
    b'-lt0B',
    b'-CD0302-',
    b'-lt0C',
    b'-lt0A4',
    b'-AZ31',
    b'-HL31',
    b'-AZ41',
    b'-KT32',
    b'-UT161',
    b'-AZ42',
    b'-TR16',
    b'-TR17',
    b'-UT185',
    b'-AZ43',
    b'-KT33',
    b'-DE12',
    b'-TR1920-',
    b'-AZ44',
    b'-UT201',
    b'-TR18',
    b'-DE13',
    b'-UT177',
    b'btpd/0.15',
    b'-UT182',
    b'-TR1540-',
    b'-TR1930-',
    b'-UT202',
    b'-TR20',
    b'-KT40',
    b'-TR210',
    b'-UT203',
    b'-AZ45',
    b'-UT204',
    b'-TR2110-',
    b'btpd/0.16',
    b'-UT220',
    b'-TR212',
    b'-TR213',
    b'-TR220',
    b'-TR221',
    b'-AZ46',
    b'-UM15',
    b'-TR222',
    b'-UT221',
    b'-KT41',
    b'-TR23',
    b'-QB26',
    b'-QB27',
    b'-QB28',
    b'-UT30',
    b'-AZ47',
    b'-TR24',
    b'-QB29',
    b'-UT31',
    b'-TR25',
    b'-KT42',
    b'-lt0D',
    b'-TR26',
    b'-UT32',
    b'-QB30',
    b'-TR27',
    b'-UM165',
    b'-KT43',
    b'-AZ48',
    b'-UM180',
    b'-UM181',
    b'-UM182',
    b'-UT33',
    b'-AZ49',
    b'-UM183',
    b'-UM184',
    b'-AZ50',
    b'-TR28',
    b'-UT331',
    b'-AZ51',
    b'-QB31',
    b'-AZ52',
    b'-AZ53',
    b'-UT34',
)


def encode_peer(peer):
    """
    Encodes a peer string (e.g., '127.0.0.1:8000') into a
    compact byte representation (e.g., b'\x7f\x00\x00\x01\x1f@')
    """
    (ip_address, port) = peer.split(':')
    compact_peer = bytes([int(s) for s in ip_address.split('.')])
    compact_peer += int(port).to_bytes(2, byteorder='big')
    return compact_peer

TORRENTS = {
    b'\x89I\x85\xf9|\xc2\\$n7\xa0|\xd7\xc7\x85\x999\x82\xa7\xcb': {
        'peers': [
            encode_peer('115.231.38.54:20302'),
            encode_peer('114.248.24.87:17099'),
        ]
    },
}


class AnnounceView(View):

    def get(self, request, auth_key):

        # Fail fast if the auth_key is invalid
        if not cache.get(auth_key):
            return self.failure('Invalid auth_key')

        # Fail fast if the client will not accept a compact response
        compact = request.GET.get('compact', '1')
        if compact == '0':
            return self.failure('This tracker only sends compact responses')

        params = dict(
            [param.split('=') for param in request.META['QUERY_STRING'].split('&')]
        )

        # These are binary values, so we have to parse them out
        info_hash = unquote_to_bytes(params.get('info_hash', b''))
        peer_id = unquote_to_bytes(params.get('peer_id', b''))

        # Fail fast if the client is not in the whitelist
        if not peer_id.startswith(PEER_ID_WHITELIST):
            return self.failure('Your client is not in the whitelist')

        # Fail fast if the torrent is not registered
        if info_hash not in TORRENTS:
            return self.failure('Unregistered torrent')

        ip = request.META['REMOTE_ADDR']
        port = request.GET.get('port')
        uploaded = request.GET.get('uploaded')
        downloaded = request.GET.get('downloaded')
        left = request.GET.get('left')
        event = request.GET.get('event')
        num_want = int(request.GET.get('numwant', '50'))
        key = request.GET.get('key')

        # Parameters we don't care about:
        #
        #    no_peer_id - We always send compact responses
        #
        #    ip - No proxy announcing allowed; we will distribute
        #        the IP from which this request originated
        #
        #    trackerid - Most clients don't implement this, and we
        #        have no use for it

        # print(params)
        # print(cache.keys('*'))

        torrent = TORRENTS[info_hash]
        peers = b''.join(torrent['peers'][:num_want])
        assert len(peers) % 6 == 0

        response_dict = {
            'interval': ANNOUNCE_INTERVAL_IN_SECONDS,
            'min interval': ANNOUNCE_INTERVAL_IN_SECONDS,
            'complete': 5,
            'incomplete': 7,
            'peers': peers,
        }

        return HttpResponse(
            'Auth key: {auth_key}<br/>'
            'User: {user}<br/>'
            'IP: {ip}<br/>'
            '<br/>Torrent: <pre>{torrent}</pre><br/>'
            '<br/>Params: <pre>{params}</pre><br/>'
            '<br/>Response: <pre>{response_dict}</pre><br/>'.format(
                auth_key=auth_key,
                user=cache.get(auth_key),
                ip=ip,
                torrent=TORRENTS.get(info_hash),
                params=pprint.pformat(params),
                response_dict=pprint.pformat(response_dict),
            )
        )

    @staticmethod
    def failure(reason):
        return HttpResponse(
            bencode(
                {
                    'failure reason': reason
                }
            )
        )
