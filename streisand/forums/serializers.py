# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from users.serializers import DisplayUserProfileSerializer
from www.templatetags.bbcode import bbcode as bbcode_to_html
from .models import ForumGroup, ForumPost, ForumThread, ForumTopic


class ForumPostSerializer(ModelSerializer):
    thread = serializers.SerializerMethodField()
    author = DisplayUserProfileSerializer()
    body_html = serializers.SerializerMethodField()

    class Meta:
        model = ForumPost
        fields = (
            'id',
            'author',
            'thread',
            'body',
            'body_html',
            'created_at',
            'modified_at',
        )

    @staticmethod
    def get_thread(forum_post):
        thread = forum_post.thread
        return {
            'id': thread.id,
            'title': thread.title,
        }

    @staticmethod
    def get_body_html(forum_post):
        return bbcode_to_html(forum_post.body)


class ForumThreadSerializer(ModelSerializer):
    latest_post = serializers.ReadOnlyField(source='last_forumpost.id')
    latest_post_created = serializers.ReadOnlyField(source='last_forumpost.created_at')
    post_count = serializers.ReadOnlyField(source='forumpost_count')
    topic_name = serializers.ReadOnlyField(source='topic.name')
    topic_id = serializers.ReadOnlyField(source='topic.id')
    subscribed_users = serializers.HiddenField(default=serializers.CurrentUserDefault()
                                               )
    posts = ForumPostSerializer(many=True, read_only=True)

    class Meta:
        model = ForumThread
        fields = ('id',
                  'topic_id',
                  'topic_name',
                  'title',
                  'created_at',
                  'created_by',
                  'posts',
                  'latest_post',
                  'latest_post_created',
                  'post_count',
                  'is_locked',
                  'is_sticky',
                  'subscribed_users'
                  )


class ForumTopicSerializer(ModelSerializer):
    latest_thread = serializers.ReadOnlyField(source='last_thread.id')
    latest_thread_title = serializers.ReadOnlyField(source='last_thread.title')
    latest_thread_created = serializers.ReadOnlyField(source='last_thread.created_at')
    thread_count = serializers.ReadOnlyField(source='forumthread_count')
    post_count = serializers.ReadOnlyField(source='forumpost_count')
    group_name = serializers.ReadOnlyField(source='group.name')
    group_id = serializers.ReadOnlyField(source='group.id')

    class Meta:
        model = ForumTopic
        fields = (
            'id',
            'sort_order',
            'name',
            'description',
            'group_name',
            'group_id',
            'minimum_user_class',
            'post_count',
            'latest_post',
            'latest_thread',
            'latest_thread_title',
            'latest_thread_created',
            'thread_count',
        )


class ForumGroupSerializer(ModelSerializer):

    topics = ForumTopicSerializer(many=True, read_only=True)

    class Meta:
        model = ForumGroup
        fields = (
            'id',
            'name',
            'sort_order',
            'topics',
        )
