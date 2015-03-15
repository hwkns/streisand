# -*- coding: utf-8 -*-

from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

from profiles.models import UserProfile

from .models import Torrent
from .forms import TorrentUploadForm


class TorrentDownloadView(View):

    def get(self, *args, **kwargs):

        # Make sure we have a valid announce key
        try:
            profile = UserProfile.objects.get(announce_key_id=kwargs['announce_key'])
        except UserProfile.DoesNotExist:
            raise PermissionDenied

        # Make sure the user can download torrents
        if not profile.user.has_perm('torrents.can_download'):
            raise PermissionDenied

        # Make sure we have a valid torrent id
        torrent = get_object_or_404(
            Torrent.objects.select_related('metainfo'),
            id=kwargs['torrent_id'],
        )

        # Respond with the customized torrent
        response = HttpResponse(
            content=torrent.metainfo.for_user_download(profile),
            content_type='application/x-bittorrent',
        )
        response['Content-Disposition'] = 'attachment; filename={release_name}.torrent'.format(
            release_name=torrent.release_name,
        )
        return response


class TorrentUploadView(View):

    def get(self, request, *args, **kwargs):

        torrent_upload_form = TorrentUploadForm(uploader=request.user.profile)
        return self._render(torrent_upload_form)

    def post(self, request, *args, **kwargs):

        if not request.user.has_perm('torrents.can_upload'):
            raise PermissionDenied("You cannot upload torrents.")

        torrent_upload_form = TorrentUploadForm(
            request.POST,
            request.FILES,
            uploader=request.user.profile,
        )

        if torrent_upload_form.is_valid():

            # Save the new Torrent object
            try:
                new_torrent = torrent_upload_form.save()
            except IntegrityError as e:
                if 'unique' in str(e):
                    torrent_upload_form.add_error('torrent_file', 'That torrent has already been uploaded')
                else:
                    raise
            else:
                return redirect(new_torrent)

        # Render the form with errors
        return self._render(torrent_upload_form)

    def _render(self, form):
        """
        Render the page with the given form.
        """
        return render(
            request=self.request,
            template_name='torrent_upload.html',
            dictionary={'form': form},
        )
