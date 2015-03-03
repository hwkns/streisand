# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .models import UserProfile


def user_profile_index(request):
    return render(
        request=request,
        template_name='user_profile_index.html',
        dictionary={
            'profiles': UserProfile.objects.all(),
        }
    )


def user_profile_redirect(request):
    profile = request.user.profile
    return HttpResponseRedirect(profile.get_absolute_url())


def user_profile_details(request, username):

    profile = get_object_or_404(
        UserProfile.objects.select_related('user').prefetch_related('torrent_stats'),
        user__username__iexact=username,
    )

    return render(
        request=request,
        template_name='user_profile_details.html',
        dictionary={
            'profile': profile,
        },
    )
