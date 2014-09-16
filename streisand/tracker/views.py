# -*- coding: utf-8 -*-

from urllib.parse import unquote_to_bytes
from binascii import b2a_hex
import pprint

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse
from django.utils.timezone import timedelta
from django.views.generic import View

from .bencoding import bencode
from .models import Peer, Swarm


class BencodedResponse(HttpResponse):
    """
    An HTTP response class that consumes data to be serialized using bencoding.
    """

    def __init__(self, data, **kwargs):
        kwargs.setdefault('content_type', 'text/plain')
        data = bencode(data)
        super(BencodedResponse, self).__init__(content=data, **kwargs)


cache.set('announce_interval_in_seconds', timedelta(minutes=40))
announce_interval_timedelta = cache.get('announce_interval_in_seconds')
ANNOUNCE_INTERVAL_IN_SECONDS = int(announce_interval_timedelta.total_seconds())

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
PEER_ID_WHITELIST = tuple(
    [
        b2a_hex(prefix).decode('ascii')
        for prefix
        in PEER_ID_WHITELIST
    ]
)

USERS = {
    '16fd2706-8baf-433b-82eb-8c7fada847da',
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
        if auth_key not in USERS:
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
            info_hash = b2a_hex(unquote_to_bytes(params['info_hash'])).decode('ascii')
            peer_id = b2a_hex(unquote_to_bytes(params['peer_id'])).decode('ascii')

        # Fail if the client is not in the whitelist
        if not peer_id.startswith(PEER_ID_WHITELIST):
            return self.failure('Your client is not in the whitelist')

        # Fail if the torrent is not registered
        try:
            torrent = Swarm.objects.get(torrent_info_hash=info_hash)
        except Swarm.DoesNotExist:
            torrent = Swarm.objects.create(torrent_info_hash=info_hash)
            # return self.failure('Unregistered torrent')

        #
        # Get announce data
        #

        # The client's IP address
        ip = request.META['REMOTE_ADDR']
        # In debug mode, allow it to be specified as a GET param
        if settings.DEBUG:
            ip = request.GET.get('ip', ip)

        # The port number that the client is listening on
        port = request.GET['port']

        # The total number of bytes uploaded since the first 'started' event
        bytes_uploaded = int(request.GET['uploaded'])

        # The total number of bytes downloaded since the first 'started' event
        bytes_downloaded = int(request.GET['downloaded'])

        # The number of bytes remaining until 100% completion
        bytes_left = int(request.GET['left'])

        # Either 'started', 'completed', or 'stopped' (optional)
        event = request.GET.get('event')

        # Number of peers the client would like to receive (optional)
        num_want = int(request.GET.get('numwant', '50'))

        # Parameters we don't care about:
        #
        #    no_peer_id - We always send compact responses
        #
        #    ip - No proxy announcing allowed; we will distribute
        #        the IP address from which this request originated
        #
        #    trackerid - Most clients don't implement this, and we
        #        have no use for it
        #
        #    key - This doesn't give us anything we don't already
        #        get from the auth_key

        # print(params)
        # print(cache.keys('*'))

        #
        # Update the peer's stats, and send signals
        #

        try:
            client = torrent.peers.get(ip_address=ip, port=port)

        except Peer.DoesNotExist:

            # Add this client to the peer list
            client = Peer.objects.create(
                swarm=torrent,
                ip_address=ip,
                port=port,
                peer_id=peer_id,
                complete=(event == 'completed') or (bytes_left == 0),
            )

        if bytes_downloaded > client.bytes_downloaded:
            # TODO: put a message in the queue that this auth_key downloaded
            # (bytes_downloaded - client.bytes_downloaded) bytes on this torrent_hash
            client.bytes_downloaded = bytes_downloaded

        if bytes_uploaded > client.bytes_uploaded:
            # TODO: put a message in the queue that this auth_key uploaded
            # (bytes_uploaded - client.bytes_uploaded) bytes on this torrent_hash
            client.bytes_uploaded = bytes_uploaded

        if event == 'started':
            # TODO: put a 'started' message in the queue
            pass
        elif event == 'stopped':
            # TODO: put a 'stopped' message in the queue
            pass
        elif event == 'completed':
            # TODO: put a 'snatched' message in the queue
            pass

        #
        # Respond to the client
        #

        # Get the peer list to send back
        if event == 'stopped':
            client.delete()
            compact_peer_list_for_client = b''
        else:
            client.save()
            compact_peer_list_for_client = b''.join(
                [bytes(peer) for peer in torrent.peers.all()][:num_want]
            )
            assert len(compact_peer_list_for_client) % 6 == 0

        # Get the number of seeders and leechers
        complete = torrent.peers.filter(complete=True).count()
        incomplete = torrent.peers.filter(complete=False).count()

        # Put everything in a dictionary
        response_dict = {
            'interval': ANNOUNCE_INTERVAL_IN_SECONDS,
            'min interval': ANNOUNCE_INTERVAL_IN_SECONDS,
            'complete': complete,
            'incomplete': incomplete,
            'peers': compact_peer_list_for_client,
        }

        if settings.DEBUG:
            return HttpResponse(
                'Auth key: {auth_key}<br/>'
                'IP: {ip}<br/>'
                '<br/>Torrent: {torrent}<br/>'
                '<br/>Peers: {peers}<br/>'
                '<br/>Request params: <pre>{params}</pre><br/>'
                '<br/>Response: <pre>{response_dict}</pre><br/>'.format(
                    auth_key=auth_key,
                    ip=ip,
                    torrent=torrent,
                    peers=torrent.peers.all(),
                    params=pprint.pformat(params),
                    response_dict=pprint.pformat(response_dict),
                )
            )
        else:
            return BencodedResponse(response_dict)

    @staticmethod
    def failure(reason):
        """
        Send a failure response to the client with the given reason.
        """
        return BencodedResponse(
            {
                'failure reason': reason
            }
        )
