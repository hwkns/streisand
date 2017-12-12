# -*- coding: utf-8 -*-

from rest_framework import serializers

from www.templatetags.bbcode import bbcode as bbcode_to_html
from .models import WikiArticle


class WikiSerializer(serializers.ModelSerializer):

    body_html = serializers.SerializerMethodField()

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
            'body_html',
            'read_access_minimum_user_class',
            'write_access_minimum_user_class',
        )

    @staticmethod
    def get_body_html(forum_post):
        return bbcode_to_html(forum_post.body)
