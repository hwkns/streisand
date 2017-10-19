# -*- coding: utf-8 -*-

from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from django.shortcuts import render, get_object_or_404

from www.utils import paginate

from .models import UserProfile
from .serializers import AdminUserProfileSerializer


class UserProfileViewSet(ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [IsAdminUser]
    queryset = UserProfile.objects.all().select_related(
        'user',
        'user_class',
        'invited_by',
    ).order_by(
        '-user__date_joined',
    )
    serializer_class = AdminUserProfileSerializer


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
