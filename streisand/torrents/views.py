# -*- coding: utf-8 -*-

from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .filters import TorrentFilter
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import View
from django_filters import rest_framework as filters

from users.models import User
from www.utils import paginate
from www.pagination import TorrentPageNumberPagination

from .forms import TorrentUploadForm
from .models import Torrent, ReseedRequest, TorrentComment
from .serializers import AdminTorrentSerializer, TorrentCommentSerializer


class TorrentCommentViewset(ModelViewSet):
    """
    API That Allows Torrent Comments to be viewed, created, or deleted. If you delete the associated film or torrent,
    The comment will be deleted as well.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TorrentCommentSerializer
    queryset = TorrentComment.objects.all().select_related(
        'torrent',
        'torrent__film',
        'author',
    ).prefetch_related('torrent', 'author').order_by('id').distinct('id')
    pagination_class = TorrentPageNumberPagination

    """
    This will automatically associate the comment author with the torrent comment on creation,
    since we already know that the comment author is the currently logged in user.
    """
    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user
        return super(TorrentCommentViewset, self).perform_create(serializer)

    def get_queryset(self):

        queryset = super().get_queryset()

        film_id = self.request.query_params.get('film_id', None)
        if film_id is not None:
            queryset = queryset.filter(film_id=film_id)

        return queryset


class TorrentViewSet(ModelViewSet):
    """
    API That currently only allows Torrents to be viewed, and searched.
    Pagination is set at Page Number Pagination, for 35 Torrents at a time for now.
    """
    permission_classes = [IsAdminUser]
    serializer_class = AdminTorrentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = TorrentFilter
    pagination_class = TorrentPageNumberPagination
    queryset = Torrent.objects.all().select_related(
        'film',
        'mediainfo',
        'source_media',
        'uploaded_by',
        'moderated_by',
    ).prefetch_related(
        'film',
        'uploaded_by',
        'moderated_by',
        'source_media',
        'mediainfo',
        'comments',
        'comments__author',
    ).order_by('id', 'source_media',).distinct('id', 'source_media',)

    def get_queryset(self):

        queryset = super().get_queryset()

        film_id = self.request.query_params.get('film_id', None)
        if film_id is not None:
            queryset = queryset.filter(film_id=film_id)

        return queryset


class TorrentDownloadView(View):

    def get(self, request, torrent_id, announce_key):

        # Make sure we have a valid announce key
        try:
            user = User.objects.get(announce_key_id=announce_key)
        except User.DoesNotExist:
            raise PermissionDenied

        # Make sure the user can download torrents
        if not user.has_perm('torrents.can_download'):
            raise PermissionDenied

        # Make sure we have a valid torrent id
        torrent = get_object_or_404(
            Torrent.objects.select_related('metainfo'),
            id=torrent_id,
        )

        # Respond with the customized torrent
        response = HttpResponse(
            content=torrent.metainfo.for_user_download(user),
            content_type='application/x-bittorrent',
        )
        response['Content-Disposition'] = 'attachment; filename={release_name}.torrent'.format(
            release_name=torrent.release_name,
        )
        return response


class TorrentUploadView(View):

    def get(self, request):

        torrent_upload_form = TorrentUploadForm(uploader=request.user)
        return self._render(torrent_upload_form)

    @method_decorator(permission_required('torrents.can_upload', raise_exception=True))
    def post(self, request):

        torrent_upload_form = TorrentUploadForm(
            request.POST,
            request.FILES,
            uploader=request.user,
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
            context={'form': form},
        )


class TorrentModerationView(View):

    @method_decorator(permission_required('torrents.can_moderate', raise_exception=True))
    def post(self, request, torrent_id):

        torrent = get_object_or_404(Torrent, id=torrent_id)

        moderation_status = request.POST['moderation_status']

        if moderation_status == 'approved':
            torrent.is_approved = True
        elif moderation_status == 'needs_work':
            torrent.is_approved = False
        else:
            torrent.is_approved = None

        torrent.moderated_by = request.user
        torrent.save()

        return redirect(torrent)


def reseed_request_index(request):

    all_reseed_requests = ReseedRequest.objects.filter(
        active_on_torrent__isnull=False,
    ).select_related(
        'created_by',
        'torrent__film',
    ).order_by(
        '-created_at',
    )

    reseed_requests = paginate(
        request=request,
        queryset=all_reseed_requests,
    )

    return render(
        request=request,
        template_name='reseed_request_index.html',
        context={
            'reseed_requests': reseed_requests,
        }
    )


@permission_required('torrents.can_request_reseed', raise_exception=True)
def new_reseed_request(request, torrent_id):

    torrent = get_object_or_404(Torrent, id=torrent_id)

    if not torrent.is_accepting_reseed_requests:
        raise PermissionDenied

    torrent.request_reseed(request.user)

    return redirect(torrent)
