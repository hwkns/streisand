# -*- coding: utf-8 -*-

from binascii import b2a_hex

from django.core.cache import cache
from django.db import models


class PeerQuerySet(models.QuerySet):

    def seeders(self):
        return self.filter(complete=True)

    def leechers(self):
        return self.filter(complete=False)

    def compact(self, limit):
        return b''.join(
            [peer.compact_bytes_repr for peer in self.all()[:limit]]
        )

class TorrentClientManager(models.Manager):

    WHITELIST_CACHE_KEY = 'client_whitelist'

    def get_whitelist(self):

        # Try to fetch the whitelist from cache
        client_whitelist = cache.get(self.WHITELIST_CACHE_KEY)

        if client_whitelist is None:

            # Create the whitelist from the database, and cache it
            client_whitelist = tuple(
                [
                    # The prefixes are in ASCII, but the rest of the peer_id can be
                    # arbitrary bytes. So we'll go ahead and transform the prefix
                    # into the format we'll be using for peer_id (a hex string) so
                    # the comparison will be faster.
                    b2a_hex(client.peer_id_prefix.encode('ascii')).decode('ascii')
                    for client
                    in self.filter(whitelisted=True)
                ]
            )
            cache.set(self.WHITELIST_CACHE_KEY, client_whitelist)

        return client_whitelist
