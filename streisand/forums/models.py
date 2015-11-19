# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.db import models

from .managers import ForumTopicManager, ForumThreadManager


class ForumGroup(models.Model):

    old_id = models.PositiveIntegerField(null=True, db_index=True)

    sort_order = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=256)

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
    )
    minimum_user_class = models.ForeignKey(
        to='user_classes.UserClass',
        related_name='unlocked_forum_topics',
        null=True,
        on_delete=models.SET_NULL,
    )
    staff_only_thread_creation = models.BooleanField(default=False)

    objects = ForumTopicManager()

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

    def is_accessible_to_user(self, user):

        if self.minimum_user_class is None:
            return True
        else:
            return self.minimum_user_class.rank <= user.profile.user_class.rank


class ForumThread(models.Model):

    old_id = models.PositiveIntegerField(null=True, db_index=True)

    title = models.CharField(max_length=1024)
    is_locked = models.BooleanField(default=False)
    is_sticky = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        to='profiles.UserProfile',
        related_name='forum_threads_created',
        null=True,  # TODO: turn this off
    )
    topic = models.ForeignKey(
        to='forums.ForumTopic',
        related_name='threads',
        null=True,  # TODO: turn this off
    )
    subscribed_users = models.ManyToManyField(
        to='profiles.UserProfile',
        through='forums.ForumThreadSubscription',
        related_name='forum_threads_subscribed',
    )

    objects = ForumThreadManager()

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
        null=True,  # TODO: turn this off
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    thread = models.ForeignKey(
        to='forums.ForumThread',
        related_name='posts',
    )

    def __str__(self):
        return 'Forum post by {author} in thread {thread}'.format(
            author=self.author,
            thread=self.thread,
        )

    def get_absolute_url(self):
        return self.thread.get_absolute_url() + '#{}'.format(self.id)


class ForumThreadSubscription(models.Model):
    profile = models.ForeignKey(
        to='profiles.UserProfile',
        related_name='forum_thread_subscriptions',
    )
    thread = models.ForeignKey(
        to='forums.ForumThread',
        related_name='subscriptions',
    )
