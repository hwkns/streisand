# -*- coding: utf-8 -*-

from celery import shared_task

from django.db.models import F

from torrents.models import Torrent

from .models import UserProfile, TorrentStats, UserIPAddress


@shared_task
def handle_announce(auth_key, swarm, new_bytes_uploaded, new_bytes_downloaded,
                    bytes_remaining, event, ip_address, port, peer_id, user_agent,
                    time_stamp):
    """
    Event handler for announces made to the tracker.

    Updates torrent stats and IP address history, using Django F expressions to
    avoid concurrency problems.  If announce logging is turned on for this profile,
    this handler logs all the announce info.
    """

    # Get the profile and the torrent that correspond to this announce
    profile = UserProfile.objects.get(auth_key_id=auth_key)
    torrent = Torrent.objects.get(swarm=swarm)

    # Get the TorrentStats relationship, or create a new one
    (torrent_stats, created) = TorrentStats.objects.get_or_create(
        profile=profile,
        torrent=torrent,
    )

    # Adjust upload and download based on multipliers
    new_bytes_downloaded = int(
        new_bytes_downloaded
        * torrent.download_multiplier
        * torrent_stats.download_multiplier
    )
    new_bytes_uploaded = int(
        new_bytes_uploaded
        * torrent.upload_multiplier
        * torrent_stats.upload_multiplier
    )

    # Update the TorrentStats
    torrent_stats.bytes_uploaded = F('bytes_uploaded') + new_bytes_uploaded
    torrent_stats.bytes_downloaded = F('bytes_downloaded') + new_bytes_downloaded
    if bytes_remaining == 0:
        torrent_stats.last_seeded = time_stamp
    torrent_stats.save()

    # Update the Torrent
    if bytes_remaining == 0:
        torrent.last_seeded = time_stamp
    if event == 'completed':
        torrent.snatch_count = F('snatch_count') + 1
    torrent.save()

    # Update the UserProfile
    if bytes_remaining == 0:
        profile.last_seeded = time_stamp
    profile.bytes_downloaded = F('bytes_downloaded') + new_bytes_downloaded
    profile.bytes_uploaded = F('bytes_uploaded') + new_bytes_uploaded
    profile.save()

    # Update the profile's IP history
    UserIPAddress.objects.update_or_create(
        profile=profile,
        ip_address=ip_address,
        used_with='tracker',
    )

    # Announce logging
    if profile.log_successful_announces:
        profile.logged_announces.create(
            time_stamp=time_stamp,
            swarm=swarm,
            auth_key=auth_key,
            ip_address=ip_address,
            port=port,
            peer_id=peer_id,
            user_agent=user_agent,
            new_bytes_downloaded=new_bytes_downloaded,
            new_bytes_uploaded=new_bytes_uploaded,
            bytes_remaining=bytes_remaining,
            event=event,
        )
