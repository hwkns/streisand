# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from www.templatetags.bbcode import bbcode as bbcode_to_html
from .models import ForumGroup, ForumPost, ForumThread, ForumTopic, ForumThreadSubscription


class ForumPostSerializer(ModelSerializer):
    topic_name = serializers.StringRelatedField(read_only=True, source='thread.topic')
    topic_id = serializers.PrimaryKeyRelatedField(read_only=True, source='thread.topic')
    thread_title = serializers.StringRelatedField(read_only=True, source='thread')
    author_id = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
    author_username = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True,
                                                     source='author')
    body_html = serializers.SerializerMethodField()

    class Meta:
        model = ForumPost
        fields = (
            'id',
            'thread',
            'thread_title',
            'topic_id',
            'topic_name',
            'author_id',
            'author_username',
            'body_html',
            'created_at',
            'modified_at',
        )

    @staticmethod
    def get_body_html(forum_post):
        return bbcode_to_html(forum_post.body)


class ForumPostForThreadSerializer(ModelSerializer):
    body_bbcode_html = serializers.SerializerMethodField()
    author_id = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
    author_username = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True,
                                                     source='author')

    class Meta:
        model = ForumPost
        fields = (
            'id',
            'author_id',
            'author_username',
            'body',
            'body_bbcode_html',
            'created_at',
            'modified_at',
        )

    @staticmethod
    def get_body_bbcode_html(forum_post):
        return bbcode_to_html(forum_post.body)


class ForumThreadSerializer(ModelSerializer):
    created_by_id = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(),
                                                       read_only=True, source='created_by'
                                                       )
    created_by = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
    topic_title = serializers.StringRelatedField(read_only=True, source='topic')
    latest_post_author_username = serializers.StringRelatedField(source='latest_post.author', read_only=True)
    latest_post_author_id = serializers.PrimaryKeyRelatedField(source='latest_post.author', read_only=True)
    posts = ForumPostForThreadSerializer(many=True, read_only=True)

    class Meta:
        model = ForumThread
        fields = (
            'id',
            'topic',
            'topic_title',
            'title',
            'created_at',
            'created_by_id',
            'created_by',
            'is_locked',
            'is_sticky',
            'number_of_posts',
            'latest_post',
            'latest_post_author_id',
            'latest_post_author_username',
            'posts',
            'subscribed_users',
        )


class ForumTopicSerializer(ModelSerializer):
    group_name = serializers.StringRelatedField(read_only=True, source='group')
    latest_post = ForumPostSerializer()
    thread_link = serializers.HyperlinkedRelatedField(many=True, read_only=True,
                                                      source='threads', view_name='forum-thread-item-detail')
    thread_title = serializers.StringRelatedField(many=True, read_only=True, source='threads')

    class Meta:
        model = ForumTopic
        fields = (
            'id',
            'sort_order',
            'name',
            'description',
            'threads',
            'thread_title',
            'thread_link',
            'group',
            'group_name',
            'minimum_user_class',
            'number_of_threads',
            'number_of_posts',
            'latest_post',
        )


class ForumTopicDataSerializer(ModelSerializer):
    latest_post_id = serializers.PrimaryKeyRelatedField(source='latest_post.id', read_only=True)
    latest_post_author_id = serializers.PrimaryKeyRelatedField(source='latest_post.author', read_only=True)
    latest_post_author_name = serializers.StringRelatedField(source='latest_post.author', read_only=True)
    latest_post_thread_id = serializers.PrimaryKeyRelatedField(source='latest_post.thread.id', read_only=True)
    latest_post_thread_title = serializers.StringRelatedField(source='latest_post.thread.title', read_only=True)
    latest_post_created_at = serializers.DateTimeField(source='latest_post.thread.created_at', read_only=True)

    class Meta:
        model = ForumTopic
        fields = (
            'id',
            'sort_order',
            'name',
            'description',
            'minimum_user_class',
            'number_of_threads',
            'number_of_posts',
            'latest_post_id',
            'latest_post_created_at',
            'latest_post_author_id',
            'latest_post_author_name',
            'latest_post_thread_id',
            'latest_post_thread_title',
        )


class ForumThreadIndexSerializer(ModelSerializer):
    group_name = serializers.StringRelatedField(read_only=True, source='topic.group')
    group_id = serializers.PrimaryKeyRelatedField(read_only=True, source='topic.group')
    created_by_id = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(),
                                                       read_only=True, source='created_by')
    created_by_username = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault(), source='created_by', read_only=True)
    topic_title = serializers.StringRelatedField(read_only=True, source='topic')
    latest_post_author_username = serializers.StringRelatedField(source='latest_post.author', read_only=True)
    latest_post_author_id = serializers.PrimaryKeyRelatedField(source='latest_post.author', read_only=True)
    latest_post_created_at = serializers.DateTimeField(source='latest_post.created_at', read_only=True)

    class Meta:
        model = ForumThread
        fields = (
            'group_id',
            'group_name',
            'topic',
            'topic_title',
            'id',
            'title',
            'created_at',
            'created_by_id',
            'created_by_username',
            'is_locked',
            'is_sticky',
            'number_of_posts',
            'latest_post',
            'latest_post_created_at',
            'latest_post_author_id',
            'latest_post_author_username',
        )


class ForumGroupSerializer(ModelSerializer):
    topic_count = serializers.IntegerField(source='topics.count')
    topics_data = ForumTopicDataSerializer(many=True, source='topics', read_only=True)

    class Meta:
        model = ForumGroup
        fields = (
            'id',
            'name',
            'sort_order',
            'topic_count',
            'topics_data',

        )


class ForumThreadSubscriptionSerializer(ModelSerializer):
    user = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True)

    class Meta:
        model = ForumThreadSubscription
        fields = ('user', 'thread')
