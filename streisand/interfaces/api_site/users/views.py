# -*- coding: utf-8 -*-

from django.contrib.auth.models import Group
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from www.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import UpdateAPIView, CreateAPIView
from .filters import UserFilter, PublicUserFilter
from www.pagination import UserPageNumberPagination
from users.models import User
from .serializers import GroupSerializer, AdminUserProfileSerializer, \
    OwnedUserProfileSerializer, PublicUserProfileSerializer, ChangePasswordSerializer, UserRegistrationSerializer, \
    UserLoginSerializer


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserRegisterView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsOwnerOrReadOnly,)

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
    # TODO: Add permissions for current userview to show for only the current user.
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
        'announce_key',
    ).prefetch_related(
        'groups',
        'torrents',
        'user_class',
        'user_permissions',
        'user_class__permissions',
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
