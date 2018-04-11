# -*- coding: utf-8 -*-

from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from .filters import UserFilter, PublicUserFilter
from www.utils import paginate
from www.pagination import UserPageNumberPagination
from .models import User
from .serializers import GroupSerializer, AdminUserProfileSerializer, \
    OwnedUserProfileSerializer, PublicUserProfileSerializer, ChangePasswordSerializer


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response("Success.", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    pagination_class = UserPageNumberPagination
    queryset = User.objects.all().select_related(
        'user_class',
    ).prefetch_related(
        'user_class', 'groups',
    ).order_by(
        '-date_joined',
    )


class AdminUserViewSet(ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited, by administrators.
    """
    permission_classes = [IsAdminUser]
    serializer_class = AdminUserProfileSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = UserFilter
    pagination_class = UserPageNumberPagination
    queryset = User.objects.all().select_related(
        'user_class',
        'invited_by',
        'auth_token',
        'announce_key',
    ).prefetch_related(
        'groups',
        'torrents',
        'user_class',
        'user_permissions',
        'user_class__permissions',
        'auth_token',
        'announce_key',
    ).order_by(
        '-date_joined', 'id',
    ).distinct('date_joined', 'id')


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
