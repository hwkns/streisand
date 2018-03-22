# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from www.templatetags.bbcode import bbcode as bbcode_to_html
from .models import ForumGroup, ForumPost, ForumThread, ForumTopic


class ForumPostSerializer(ModelSerializer):
    topic_name = serializers.StringRelatedField(read_only=True, source='thread.topic')
    topic_id = serializers.PrimaryKeyRelatedField(read_only=True, source='thread.topic')
    thread_title = serializers.StringRelatedField(read_only=True, source='thread')
    author = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
    body_html = serializers.SerializerMethodField()

    class Meta:
        model = ForumPost
        fields = (
            'id',
            'thread',
            'thread_title',
            'topic_id',
            'topic_name',
            'author',
            'body',
            'body_html',
            'created_at',
            'modified_at',
        )

    @staticmethod
    def get_body_html(forum_post):
        return bbcode_to_html(forum_post.body)


class ForumThreadSerializer(ModelSerializer):
    created_by = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
    latest_post = ForumPostSerializer()
    topic_title = serializers.StringRelatedField(read_only=True, source='topic')

    class Meta:
        model = ForumThread
        fields = (
            'id',
            'topic',
            'topic_title',
            'title',
            'created_at',
            'created_by',
            'is_locked',
            'is_sticky',
            'number_of_posts',
            'latest_post',
        )


class ForumTopicSerializer(ModelSerializer):

    group_name = serializers.StringRelatedField(read_only=True, source='group')
    latest_post = ForumPostSerializer()

    class Meta:
        model = ForumTopic
        fields = (
            'id',
            'sort_order',
            'name',
            'description',
            'threads',
            'group',
            'group_name',
            'minimum_user_class',
            'number_of_threads',
            'number_of_posts',
            'latest_post',
        )


class ForumGroupSerializer(ModelSerializer):

    topic_name = serializers.StringRelatedField(many=True, read_only=True, source='topics')

    class Meta:
        model = ForumGroup
        fields = (
            'id',
            'name',
            'sort_order',
            'topics',
            'topic_name',
        )
