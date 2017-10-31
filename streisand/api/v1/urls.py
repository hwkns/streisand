# -*- coding: utf-8 -*-

from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from django.conf.urls import url, include

from films.views import FilmViewSet
from profiles.views import UserProfileViewSet
from torrents.views import TorrentViewSet
from www.views import UserViewSet, GroupViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'profiles', UserProfileViewSet)
router.register(r'films', FilmViewSet)
router.register(r'torrents', TorrentViewSet)

urlpatterns = [

    # Router URLs
    url(r'^', include(router.urls)),
    url(r'^auth', obtain_auth_token),

    # DRF browsable API
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]
