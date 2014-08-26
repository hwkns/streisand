# -*- coding: utf-8 -*-

from urllib.parse import unquote_to_bytes
from binascii import b2a_hex, a2b_hex
import pprint

from django.views.generic import View
from django.http import HttpResponse
from django.core.cache import cache
from django.utils.timezone import now, timedelta

from .bencoding import bencode


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


class Peer(object):

    # TODO: put completed and uncompleted peers in separate lists under
    # the torrent so it's quicker to find the length of them

    def __init__(self, ip, port, last_modified, uploaded=0, downloaded=0, completed=False):
        self.ip = ip
        self.port = port
        self.last_modified = last_modified
        self.uploaded = uploaded
        self.downloaded = downloaded
        self.completed = completed

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '{ip}:{port}'.format(
            ip=self.ip,
            port=self.port,
        )


def encode_peer(ip, port):
    """
    Encodes a peer string (e.g., '127.0.0.1:8000') into a
    compact byte representation (e.g., b'\x7f\x00\x00\x01\x1f@')
    """
    compact_peer = bytes([int(s) for s in ip.split('.')])
    compact_peer += int(port).to_bytes(2, byteorder='big')
    return compact_peer


TORRENTS = {
    b2a_hex(b'\x89I\x85\xf9|\xc2\\$n7\xa0|\xd7\xc7\x85\x999\x82\xa7\xcb'): {
        encode_peer(ip='115.231.38.54', port='20302'): Peer(
            ip='115.231.38.54',
            port='20302',
            last_modified=now(),
            completed=True,
        ),
        encode_peer(ip='114.248.24.87', port='17099'): Peer(
            ip='114.248.24.87',
            port='17099',
            last_modified=now(),
            completed=True,
        ),
    },
}

USERS = {
    '16fd2706-8baf-433b-82eb-8c7fada847da': {
        'username': 'hwkns',
        'torrents': {
            b2a_hex(b'\x89I\x85\xf9|\xc2\\$n7\xa0|\xd7\xc7\x85\x999\x82\xa7\xcb'),
        },
        'uploaded': 0,
        'downloaded': 0,
    }
}


class AnnounceView(View):

    REQUIRED_PARAMS = {
        'info_hash',
        'peer_id',
        'port',
        'uploaded',
        'downloaded',
        'left',
    }

    def get(self, request, auth_key):

        #
        # Short circuit bad requests
        #

        # Fail if the auth_key is invalid
        user = USERS.get(auth_key)
        if not user:
            return self.failure('Invalid auth_key')

        # Fail if the client will not accept a compact response
        compact = request.GET.get('compact', '1')
        if compact == '0':
            return self.failure('This tracker only sends compact responses')

        # Fail if any required parameters are missing
        if not self.REQUIRED_PARAMS <= request.GET.keys():
            return self.failure('Announce request was missing one or more required parameters')

        # The `info_hash` and `peer_id` parameters include raw bytes, and
        # Django irreversibly encodes them into strings for request.GET,
        # so we have to parse them out of the QUERY_STRING header.  >.<
        try:
            params = dict(
                [param.split('=') for param in request.META['QUERY_STRING'].split('&')]
            )
        except Exception:
            return self.failure('Announce request contained malformed GET parameters')
        else:
            info_hash = unquote_to_bytes(params['info_hash'])
            peer_id = unquote_to_bytes(params['peer_id'])

        # Fail if the client is not in the whitelist
        if not peer_id.startswith(PEER_ID_WHITELIST):
            return self.failure('Your client is not in the whitelist')

        # Fail if the torrent is not registered
        peers = TORRENTS.get(b2a_hex(info_hash))
        if not peers:
            return self.failure('Unregistered torrent')

        #
        # Get announce data
        #

        # The client's IP address
        ip = request.META['REMOTE_ADDR']

        # The port number that the client is listening on
        port = request.GET['port']

        # The total number of bytes uploaded since the first 'started' event
        uploaded = int(request.GET['uploaded'])

        # The total number of bytes downloaded since the first 'started' event
        downloaded = int(request.GET['downloaded'])

        # The number of bytes remaining until 100% completion
        left = int(request.GET['left'])

        # Either 'started', 'completed', or 'stopped' (optional)
        event = request.GET.get('event')

        # Number of peers the client would like to receive (optional)
        num_want = int(request.GET.get('numwant', '50'))

        # Parameters we don't care about:
        #
        #    no_peer_id - We always send compact responses
        #
        #    ip - No proxy announcing allowed; we will distribute
        #        the IP from which this request originated
        #
        #    trackerid - Most clients don't implement this, and we
        #        have no use for it
        #
        #    key - This doesn't give us anything we don't already
        #        get from the auth_key

        # print(params)
        # print(cache.keys('*'))

        # Add the client to the peer list
        client = encode_peer(ip=ip, port=port)
        if event == 'stopped':
            if client in peers:
                del peers[client]
        else:
            if client in peers:
                # Update this client's peer list entry
                peer = peers[client]
                if peer.downloaded < downloaded:
                    # TODO: async update the user's total downloaded amount
                    pass
                if peer.uploaded < uploaded:
                    # TODO: async update the user's total uploaded amount
                    peer.uploaded = uploaded
            else:
                # Add this client to the peer list
                peers[client] = Peer(
                    ip=ip,
                    port=port,
                    last_modified=now(),
                    uploaded=uploaded,
                    downloaded=downloaded,
                    completed=(event == 'completed') or (left == 0),
                )

        # Get the peer list to send back to the client
        compact_peer_list_for_client = b''.join(
            [peer for peer in peers.keys()][:num_want]
        )
        assert len(compact_peer_list_for_client) % 6 == 0

        # Get the number of seeders and leechers
        complete = len([peer for peer in peers if peers[peer].completed])
        incomplete = len(peers) - complete

        response_dict = {
            'interval': ANNOUNCE_INTERVAL_IN_SECONDS,
            'min interval': ANNOUNCE_INTERVAL_IN_SECONDS,
            'complete': complete,
            'incomplete': incomplete,
            'peers': compact_peer_list_for_client,
        }

        return HttpResponse(
            'Auth key: {auth_key}<br/>'
            'User: {user}<br/>'
            'IP: {ip}<br/>'
            '<br/>Torrent: <pre>{torrent}</pre><br/>'
            '<br/>Params: <pre>{params}</pre><br/>'
            '<br/>Response: <pre>{response_dict}</pre><br/>'.format(
                auth_key=auth_key,
                user=user,
                ip=ip,
                torrent=peers,
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
