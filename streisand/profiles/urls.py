# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^/?$', views.user_profile_index, name='user_profile_index'),
    url(r'^(?P<username>.+)/?$', views.user_profile_details, name='user_profile'),
]
