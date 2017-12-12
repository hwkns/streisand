# -*- coding: utf-8 -*-

from django.db import models
from django.urls import reverse

from .managers import ForumGroupQuerySet, ForumTopicQuerySet, ForumThreadQuerySet


class ForumGroup(models.Model):

    old_id = models.PositiveIntegerField(null=True, db_index=True)

    sort_order = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=256)

    objects = ForumGroupQuerySet.as_manager()

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return '{name}'.format(name=self.name)


class ForumTopic(models.Model):

    old_id = models.PositiveIntegerField(null=True, db_index=True)

    sort_order = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=1024)
    group = models.ForeignKey(
        to='forums.ForumGroup',
        related_name='topics',
        null=False,
        on_delete=models.PROTECT,
    )
    minimum_user_class = models.ForeignKey(
        to='user_classes.UserClass',
        related_name='unlocked_forum_topics',
        null=True,
        on_delete=models.SET_NULL,
    )
    staff_only_thread_creation = models.BooleanField(default=False)
    number_of_threads = models.PositiveIntegerField(default=0)
    number_of_posts = models.PositiveIntegerField(default=0)
    latest_post = models.OneToOneField(
        to='forums.ForumPost',
        related_name='topic_latest',
        null=True,
        on_delete=models.SET_NULL,
    )

    objects = ForumTopicQuerySet.as_manager()

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return '{name}'.format(name=self.name)

    def get_absolute_url(self):
        return reverse(
            viewname='forum_topic_details',
            kwargs={
                'topic_id': self.id,
            }
        )


class ForumThread(models.Model):

    old_id = models.PositiveIntegerField(null=True, db_index=True)

    title = models.CharField(max_length=1024)
    is_locked = models.BooleanField(default=False)
    is_sticky = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        to='profiles.UserProfile',
        related_name='forum_threads_created',
        null=True,
        on_delete=models.SET_NULL,
    )
    topic = models.ForeignKey(
        to='forums.ForumTopic',
        related_name='threads',
        null=False,
        on_delete=models.PROTECT,
    )
    number_of_posts = models.PositiveIntegerField(default=0)
    latest_post = models.OneToOneField(
        to='forums.ForumPost',
        related_name='thread_latest',
        null=True,
        on_delete=models.SET_NULL,
    )
    subscribed_users = models.ManyToManyField(
        to='profiles.UserProfile',
        through='forums.ForumThreadSubscription',
        related_name='forum_threads_subscribed',
    )

    class Meta:
        get_latest_by = 'created_at'

    objects = ForumThreadQuerySet.as_manager()

    def __str__(self):
        return '{title}'.format(title=self.title)

    def get_absolute_url(self):
        return reverse(
            viewname='forum_thread_details',
            kwargs={
                'thread_id': self.id,
            }
        )


class ForumPost(models.Model):

    old_id = models.PositiveIntegerField(null=True, db_index=True)

    author = models.ForeignKey(
        to='profiles.UserProfile',
        related_name='forum_posts',
        null=True,
        on_delete=models.PROTECT,
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    thread = models.ForeignKey(
        to='forums.ForumThread',
        related_name='posts',
        on_delete=models.CASCADE,
    )

    class Meta:
        get_latest_by = 'created_at'

    def __str__(self):
        return 'Forum post by {author} in thread {thread}'.format(
            author=self.author,
            thread=self.thread,
        )

    def get_absolute_url(self):
        return '{thread_url}#{post_id}'.format(
            thread_url=self.thread.get_absolute_url(),
            post_id=self.id,
        )


class ForumThreadSubscription(models.Model):
    profile = models.ForeignKey(
        to='profiles.UserProfile',
        related_name='forum_thread_subscriptions',
        on_delete=models.CASCADE,
    )
    thread = models.ForeignKey(
        to='forums.ForumThread',
        related_name='subscriptions',
        on_delete=models.CASCADE,
    )
