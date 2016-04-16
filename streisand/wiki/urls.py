# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        regex=r'^$',
        view=views.wiki_index,
        name='wiki_index',
    ),
    url(
        regex=r'^(?P<wiki_page_slug>.+)/$',
        view=views.WikiPageView.as_view(),
        name='wiki_page',
    ),
    url(
        regex=r'^new/$',
        view=views.NewWikiPageView.as_view(),
        name='new_wiki_page',
    ),
]
