# -*- coding: utf-8 -*-

from celery import shared_task
from pytz import UTC

from django.db.models import F
from django.utils.timezone import datetime

from torrents.models import Torrent

from .models import UserProfile, TorrentStats, UserIPAddress


@shared_task
def handle_announce(auth_key, info_hash, new_bytes_uploaded, new_bytes_downloaded,
                    bytes_remaining, event, ip_address, port, peer_id, user_agent,
                    time_stamp):
    """
    Event handler for announces made to the tracker.

    Updates torrent stats and IP address history, using Django F expressions to
    avoid concurrency problems.  If announce logging is turned on for this profile,
    this handler logs all the announce info.
    """

    time_stamp = datetime.fromtimestamp(time_stamp).replace(tzinfo=UTC)

    # Get the profile and the torrent that correspond to this announce
    profile = UserProfile.objects.get(auth_key=auth_key)
    torrent = Torrent.objects.get(info_hash=info_hash)

    # Create or update the relevant TorrentStats object
    (torrent_stats, created) = TorrentStats.objects.get_or_create(
        profile=profile,
        torrent=torrent,
    )
    torrent_stats.bytes_uploaded = F('bytes_uploaded') + new_bytes_uploaded
    torrent_stats.bytes_downloaded = F('bytes_downloaded') + new_bytes_downloaded
    if event == 'completed':
        torrent_stats.snatch_count = F('snatch_count') + 1
    torrent_stats.save()

    # Update the UserProfile
    profile.bytes_downloaded = F('bytes_downloaded') + new_bytes_downloaded
    profile.bytes_uploaded = F('bytes_uploaded') + new_bytes_uploaded
    profile.save()

    # Update IP history
    UserIPAddress.objects.update_or_create(
        profile=profile,
        ip_address=ip_address,
        used_with='tracker',
    )

    # Announce logging
    if profile.log_successful_announces:
        profile.logged_announces.create(
            time_stamp=time_stamp,
            auth_key=auth_key,
            info_hash=info_hash,
            ip_address=ip_address,
            port=port,
            peer_id=peer_id,
            user_agent=user_agent,
            new_bytes_downloaded=new_bytes_downloaded,
            new_bytes_uploaded=new_bytes_uploaded,
            bytes_remaining=bytes_remaining,
            event=event,
        )
