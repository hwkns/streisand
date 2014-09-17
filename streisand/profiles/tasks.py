# -*- coding: utf-8 -*-

from celery import shared_task

from django.db.models import F

from torrents.models import Torrent

from .models import UserProfile, TorrentStats


@shared_task
def handle_announce(auth_key, info_hash, peer_id, ip_address, port,
                    new_bytes_uploaded, new_bytes_downloaded, event):
    """
    Event handler for announces made to the tracker.

    Uses Django F expressions to avoid concurrency problems.
    """
    # TODO: user agent, bytes_remaining

    profile = UserProfile.objects.get(auth_key=auth_key)
    torrent = Torrent.objects.get(info_hash=info_hash)
    (torrent_stats, created) = TorrentStats.objects.get_or_create(
        profile=profile,
        torrent=torrent,
    )

    torrent_stats.bytes_uploaded = F('bytes_uploaded') + new_bytes_uploaded

    # if not torrent.freeleech:
    torrent_stats.bytes_downloaded = F('bytes_downloaded') + new_bytes_downloaded

    torrent_stats.save()
