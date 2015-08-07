# -*- coding: utf-8 -*-

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

from .models import UserProfile


def user_profile_index(request):

    all_user_profiles = UserProfile.objects.filter(
        account_status='enabled',
    ).select_related(
        'user',
    )

    # Show 50 requests per page
    paginator = Paginator(all_user_profiles, 50)

    page = request.GET.get('page')
    try:
        user_profiles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        user_profiles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        user_profiles = paginator.page(paginator.num_pages)

    return render(
        request=request,
        template_name='user_profile_index.html',
        dictionary={
            'profiles': user_profiles,
        }
    )


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
