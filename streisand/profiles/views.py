# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404

from www.utils import paginate

from .models import UserProfile


def user_profile_index(request):

    user_profiles = paginate(
        request=request,
        queryset=UserProfile.objects.filter(
            account_status='enabled',
        ).select_related(
            'user',
        )
    )

    return render(
        request=request,
        template_name='user_profile_index.html',
        context={
            'profiles': user_profiles,
        }
    )


def user_profile_details(request, username):

    profile = get_object_or_404(
        UserProfile.objects.select_related('user'),
        user__username__iexact=username,
    )

    return render(
        request=request,
        template_name='user_profile_details.html',
        context={
            'profile': profile,
        },
    )
