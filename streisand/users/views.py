# -*- coding: utf-8 -*-

from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters
from rest_framework.views import APIView
from .filters import UserFilter, PublicUserFilter
from www.utils import paginate
from .models import User
from .serializers import GroupSerializer, AdminUserProfileSerializer, OwnedUserProfileSerializer, PublicUserProfileSerializer


class CurrentUserView(APIView):
    def get(self, request):
        serializer = OwnedUserProfileSerializer(request.user)
        return Response(serializer.data)


class PublicUserProfileViewSet(ModelViewSet):
    """
    API endpoint that allows users to be viewed and searched only.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PublicUserProfileSerializer
    http_method_names = ['get', 'head', 'options']
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = PublicUserFilter
    queryset = User.objects.all().select_related(
        'user_class',
    ).prefetch_related(
        'user_class', 'groups',
    ).order_by(
        '-date_joined',
    )


class UserViewSet(ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited, by administrators.
    """
    permission_classes = [IsAdminUser]
    serializer_class = AdminUserProfileSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = UserFilter
    queryset = User.objects.all().select_related(
        'user_class',
        'invited_by',
    ).prefetch_related(
        'groups',
    ).order_by(
        '-date_joined',
    )


class GroupViewSet(ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = [IsAdminUser]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


def user_profile_index(request):

    users = paginate(
        request=request,
        queryset=User.objects.filter(account_status='enabled'),
    )

    return render(
        request=request,
        template_name='user_profile_index.html',
        context={
            'users': users,
        }
    )


def user_profile_details(request, username):

    user = get_object_or_404(
        User.objects.all(),
        username__iexact=username,
    )

    return render(
        request=request,
        template_name='user_profile_details.html',
        context={
            'user': user,
        },
    )
