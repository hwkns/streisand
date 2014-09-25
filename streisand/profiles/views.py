# -*- coding: utf-8 -*-

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

from .models import UserProfile


def index(request):
    return render(
        request=request,
        template_name='profiles.html',
        dictionary={
            'profiles': UserProfile.objects.all(),
        }
    )


def user_profile_redirect(request):
    profile = request.user.profile
    return HttpResponseRedirect(profile.get_absolute_url())


def user_profile(request, profile_id):

    try:
        profile = UserProfile.objects.filter(
            id=profile_id
        ).select_related(
            'user'
        ).prefetch_related(
            'torrent_stats'
        ).get()
    except UserProfile.DoesNotExist:
        raise Http404

    return render(
        request=request,
        template_name='profile.html',
        dictionary={
            'profile': profile,
        },
    )
