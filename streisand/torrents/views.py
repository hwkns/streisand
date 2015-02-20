# -*- coding: utf-8 -*-

from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

from tracker.bencoding import bencode

from .models import Torrent
from .forms import TorrentUploadForm


def torrent_index(request):
    return render(
        request=request,
        template_name='torrent_index.html',
        dictionary={
            'torrents': Torrent.objects.all(),
        }
    )


def torrent_details(request, torrent_id):
    torrent = get_object_or_404(
        Torrent.objects.select_related('film'),
        id=torrent_id,
    )
    return render(
        request=request,
        template_name='torrent_details.html',
        dictionary={
            'torrent': torrent,
        }
    )


def torrent_download(request, torrent_id):
    torrent = get_object_or_404(Torrent, id=torrent_id)
    content = bencode(torrent.metadata_dict)
    response = HttpResponse(content, content_type='application/x-bittorrent')
    response['Content-Disposition'] = 'attachment; filename={name}.torrent'.format(name=torrent.release_name)
    return response


class TorrentUploadView(View):

    def dispatch(self, request, *args, **kwargs):

        if request.user.has_perm('torrents.upload'):
            return super(TorrentUploadView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You cannot upload torrents.")

    def get(self, request, *args, **kwargs):

        torrent_upload_form = TorrentUploadForm(uploader=request.user.profile)
        return self._render(torrent_upload_form)

    def post(self, request, *args, **kwargs):

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
                return redirect(new_torrent.get_absolute_url())

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
