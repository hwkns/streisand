# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import WikiArticle


class WikiSerializer(serializers.ModelSerializer):

    class Meta:
        model = WikiArticle
        fields = (
            'id',
            'created_at',
            'created_by',
            'modified_at',
            'modified_by',
            'title',
            'body',
            'read_access_minimum_user_class',
            'write_access_minimum_user_class',
        )
