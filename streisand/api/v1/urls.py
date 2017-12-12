# -*- coding: utf-8 -*-

from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from django.conf.urls import url, include

from films.views import FilmViewSet
from profiles.views import UserProfileViewSet
from torrents.views import TorrentViewSet
from www.views import UserViewSet, GroupViewSet
from forums.views import ForumGroupViewSet, ForumTopicViewSet, ForumThreadViewSet, ForumPostViewSet, NewsPostViewSet
from wiki.views import WikiArticleViewSet

router = routers.DefaultRouter()
router.register(r'users', viewset=UserViewSet)
router.register(r'groups', viewset=GroupViewSet)
router.register(r'profiles', viewset=UserProfileViewSet)
router.register(r'films', viewset=FilmViewSet)
router.register(r'torrents', viewset=TorrentViewSet)
router.register(r'forum-groups', viewset=ForumGroupViewSet, base_name='forum-group')
router.register(r'forum-topics', viewset=ForumTopicViewSet, base_name='forum-topic')
router.register(r'forum-threads', viewset=ForumThreadViewSet, base_name='forum-thread')
router.register(r'forum-posts', viewset=ForumPostViewSet, base_name='forum-post')
router.register(r'news-posts', viewset=NewsPostViewSet, base_name='news-post')
router.register(r'wiki-articles', viewset=WikiArticleViewSet, base_name='wiki-article')


urlpatterns = [

    # Router URLs
    url(r'^', include(router.urls)),
    url(r'^auth', obtain_auth_token),

    # DRF browsable API
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]
