# -*- coding: utf-8 -*-

import json
import logging

from django.contrib.auth import authenticate, login
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

from films.models import Film
from film_lists.models import FilmList
from forums.models import ForumThread
from profiles.models import UserProfile
from torrents.models import Torrent

from .forms import RegistrationForm
from .models import Feature


def home(request):
    news_thread = ForumThread.objects.filter(topic__name='Announcements').latest()
    news_post = news_thread.posts.earliest()
    return render(
        request=request,
        template_name='home.html',
        dictionary={
            'news_post': news_post,
        }
    )


class RegistrationView(View):

    form = RegistrationForm()
    invite_key = None

    def dispatch(self, request, *args, **kwargs):

        if not Feature.objects.is_enabled('open_registration'):
            raise Http404

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return self.render_form()

    def post(self, request):

        self.form = RegistrationForm(request.POST)

        if self.form.is_valid():

            # Flag potential dupers
            if request.user.is_authenticated():
                log = logging.getLogger('streisand.security')
                log.warning(
                    'New user "{new_user}" registered while logged in as '
                    'existing user "{existing_user}".'.format(
                        new_user=self.form.cleaned_data['username'],
                        existing_user=request.user.username,
                    )
                )

            self.form.save()

            # Authenticate the newly registered user
            new_authenticated_user = authenticate(
                username=self.form.cleaned_data['username'],
                password=self.form.cleaned_data['password1'],
            )
            login(request, new_authenticated_user)
            return redirect('home')

        else:

            return self.render_form()

    def render_form(self):
        return render(
            request=self.request,
            template_name='register.html',
            dictionary={'form': self.form},
        )


class LegacyURLView(View):
    """
    This view provides support for old URLs so users have time to
    update their bookmarks.

    Each section of the old site has its own method, which will
    return a permanent redirect to the equivalent part of the new site.
    """

    def get(self, request, section):
        if hasattr(self, section):
            return getattr(self, section)(request)
        else:
            return redirect('home')

    def forums(self, request):
        pass

    def inbox(self, request):
        pass

    def montage(self, request):

        if 'id' not in request.GET:
            return redirect('film_list_index')

        film_list = get_object_or_404(FilmList, old_id=request.GET['id'])
        return redirect(film_list)

    def peoples(self, request):
        pass

    def queue(self, request):

        if 'user' in request.GET:
            profile = get_object_or_404(UserProfile, old_id=request.GET['user'])
        else:
            profile = request.user.profile
        return redirect(profile.watch_queue)

    def requests(self, request):
        pass

    def reseed(self, request):
        pass

    def rules(self, request):
        pass

    def staffpm(self, request):
        pass

    def top10(self, request):
        pass

    def torrents(self, request):

        if 'id' not in request.GET:
            return redirect('film_index')

        # Torrents
        if 'torrentid' in request.GET:
            try:
                torrent = Torrent.objects.get(old_id=request.GET['torrentid'])
            except Torrent.DoesNotExist:
                pass
            else:
                return redirect(torrent)

        # FilmLists
        elif 'montage' in request.GET:
            get_object_or_404(FilmList, old_id=request.GET['montage'])

        # Films
        film = get_object_or_404(Film, old_id=request.GET['id'])
        return redirect(film)

    def user(self, request):

        if 'id' not in request.GET:
            # TODO: torrent notifications?  https://tehconnection.eu/user.php?action=notify
            return redirect('profile_index')

        # UserProfiles
        profile = get_object_or_404(UserProfile, old_id=request.GET['id'])
        return redirect(profile)

    def wiki(self, request):
        pass


def template_viewer(request, template_path):
    return render(request, template_path, json.loads(request.GET.get('context', '{}')))
