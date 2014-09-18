# -*- coding: utf-8 -*-

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


def profile_view(request, profile_id):
    profile = UserProfile.objects.filter(id=profile_id).select_related('user').get()
    return render(
        request=request,
        template_name='profile.html',
        dictionary={
            'profile': profile,
        },
    )
