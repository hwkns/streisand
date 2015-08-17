# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.film_list_index, name='film_list_index'),
    url(r'^(?P<film_list_id>\d+)/$', views.film_list_details, name='film_list_details'),
]
