# -*- coding: utf-8 -*-
from django.contrib.auth.models import Group
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from rest_framework.renderers import BrowsableAPIRenderer
from www.permissions import IsAccountOwner
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.generics import UpdateAPIView, RetrieveAPIView, CreateAPIView
from .filters import UserFilter, PublicUserFilter
from www.pagination import UserPageNumberPagination
from users.models import User
from .serializers import GroupSerializer, AdminUserProfileSerializer, \
    OwnedUserProfileSerializer, PublicUserProfileSerializer, ChangePasswordSerializer, NewUserSerializer, \
    MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class UserRegisterView(CreateAPIView):
    """
    Register a new user.
    """
    serializer_class = NewUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web token pair,
    to prove the authentication of those credentials.
    """
    serializer_class = MyTokenObtainPairSerializer
    renderer_classes = (CamelCaseJSONRenderer, BrowsableAPIRenderer)


# class UserRegisterView(CreateAPIView):
#     serializer_class = UserRegistrationSerializer
#     queryset = User.objects.all()
#     permission_classes = [AllowAny]


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAccountOwner]

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


class CurrentUserView(RetrieveAPIView):
    serializer_class = OwnedUserProfileSerializer
    permission_classes = [IsAccountOwner]

    def get_queryset(self):
        return User.objects.filter(user=self.request.user)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj


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
