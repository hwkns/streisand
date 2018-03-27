# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from films.views import FilmViewSet, CollectionViewSet, CollectionCommentViewSet, FilmCommentViewSet
from forums.views import ForumGroupViewSet, ForumTopicViewSet, ForumThreadIndexViewSet, ForumThreadWithAllPostsViewSet, \
    ForumThreadItemViewSet, ForumPostViewSet, NewsPostViewSet, ForumThreadSubscriptionViewSet
from torrents.views import TorrentViewSet
from users.views import UserViewSet, GroupViewSet, CurrentUserView
from wiki.views import WikiArticleCreateUpdateDestroyViewSet, WikiArticleBodyViewSet, WikiArticleViewListOnlyViewSet

router = routers.DefaultRouter()
router.register(r'users', viewset=UserViewSet, base_name='user')
router.register(r'groups', viewset=GroupViewSet, base_name='group')
router.register(r'films', viewset=FilmViewSet, base_name='film')
router.register(r'film-comments', viewset=FilmCommentViewSet, base_name='film-comment')
router.register(r'collections', viewset=CollectionViewSet, base_name='collection')
router.register(r'collection-comments', viewset=CollectionCommentViewSet, base_name='collection-comment')
router.register(r'torrents', viewset=TorrentViewSet, base_name='torrent')
router.register(r'forum-groups', viewset=ForumGroupViewSet, base_name='forum-group')
router.register(r'forum-topics', viewset=ForumTopicViewSet, base_name='forum-topic')
router.register(r'forum-thread-index', viewset=ForumThreadIndexViewSet, base_name='forum-thread-index')
router.register(r'forum-threads', viewset=ForumThreadWithAllPostsViewSet, base_name='forum-thread')
router.register(r'forum-thread-items', viewset=ForumThreadItemViewSet, base_name='forum-thread-item')
router.register(r'forum-thread-subscriptions', viewset=ForumThreadSubscriptionViewSet,
                base_name='forum-thread-subscription')
router.register(r'forum-posts', viewset=ForumPostViewSet, base_name='forum-post')
router.register(r'news-posts', viewset=NewsPostViewSet, base_name='news-post')
router.register(r'wikis', viewset=WikiArticleCreateUpdateDestroyViewSet, base_name='wiki')
router.register(r'wiki-articles', viewset=WikiArticleViewListOnlyViewSet, base_name='wiki-article')
router.register(r'wiki-bodies', viewset=WikiArticleBodyViewSet, base_name='wiki-body')

urlpatterns = [

    # Router URLs
    url(r'^', include(router.urls)),
    url(r'^auth', obtain_auth_token),

    # DRF browsable API
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^current-user/', CurrentUserView.as_view()),


]
