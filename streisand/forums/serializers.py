# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from profiles.serializers import DisplayUserProfileSerializer
from .models import ForumGroup, ForumPost, ForumThread, ForumTopic


class ForumPostSerializer(ModelSerializer):

    thread = serializers.SerializerMethodField()
    author = DisplayUserProfileSerializer()

    class Meta:
        model = ForumPost
        fields = (
            'id',
            'author',
            'thread',
            'body',
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


class ForumThreadSerializer(ModelSerializer):

    latest_post = ForumPostSerializer()

    class Meta:
        model = ForumThread
        fields = (
            'id',
            'topic',
            'title',
            'created_at',
            'created_by',
            'is_locked',
            'is_sticky',
            'number_of_posts',
            'latest_post',
        )


class ForumTopicSerializer(ModelSerializer):

    group = serializers.SerializerMethodField()
    latest_post = ForumPostSerializer()

    class Meta:
        model = ForumTopic
        fields = (
            'id',
            'sort_order',
            'name',
            'description',
            'group',
            'minimum_user_class',
            'number_of_threads',
            'number_of_posts',
            'latest_post',
        )

    @staticmethod
    def get_group(forum_topic):
        group = forum_topic.group
        return {
            'id': group.id,
            'name': group.name,
        }


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
