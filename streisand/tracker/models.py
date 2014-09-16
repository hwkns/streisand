# -*- coding: utf-8 -*-

from django.db import models

from django_extensions.db.fields import UUIDField


class Swarm(models.Model):
    # TODO: make a custom field type for this
    torrent_info_hash = models.CharField(max_length=40, primary_key=True)

    def __str__(self):
        return self.torrent_info_hash

    def __repr__(self):
        return self.__str__()


class Peer(models.Model):
    """
    A peer in a particular torrent swarm.
    """

    # Because Django does not support compound primary keys, and because this
    # table might actually hit the max limit of an auto-incrementing integer ID,
    # we use an auto-generated UUIDField as the primary key.
    id = UUIDField(auto=True, primary_key=True, editable=False)

    swarm = models.ForeignKey(Swarm, related_name='peers')
    user_auth_key = models.CharField(max_length=36)
    peer_id = models.CharField(max_length=40)
    ip_address = models.GenericIPAddressField()
    port = models.CharField(max_length=5)

    # These are checked by the tracker when the client announces again,
    # to decide whether the user's upload/download should be increased
    bytes_uploaded = models.BigIntegerField(default=0)
    bytes_downloaded = models.BigIntegerField(default=0)

    complete = models.BooleanField(default=False)

    first_announce = models.DateTimeField(auto_now_add=True)
    last_announce = models.DateTimeField(auto_now=True)

    class Meta:
        # Two clients, sharing an IP address and seeding the same torrent for the
        # same user, could swap ports between announces due to a restart.
        unique_together = ['swarm', 'user_auth_key', 'ip_address', 'port']

    def __bytes__(self):
        compact_ip = bytes([int(s) for s in self.ip_address.split('.')])
        compact_port = int(self.port).to_bytes(2, byteorder='big')
        return compact_ip + compact_port

    def __str__(self):
        return '{ip}:{port}'.format(
            ip=self.ip_address,
            port=self.port,
        )

    def __repr__(self):
        return self.__str__()
