# -*- coding: utf-8 -*-

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from collections import OrderedDict

from django.db.models import OuterRef, Subquery
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from www.utils import paginate

from .forms import ForumPostForm
from .models import ForumGroup, ForumTopic, ForumThread, ForumPost
from .serializers import (
    ForumGroupSerializer,
    ForumTopicSerializer,
    ForumThreadSerializer,
    ForumPostSerializer,
)


class ForumGroupViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = ForumGroupSerializer
    queryset = ForumGroup.objects.all().prefetch_related(
        'topics__latest_post__author',
        'topics__latest_post__author__user_class',
        'topics__latest_post__thread',
    )

    def get_queryset(self):
        return super().get_queryset().accessible_to_user(self.request.user)


class ForumTopicViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = ForumTopicSerializer
    queryset = ForumTopic.objects.all().select_related(
        'group',
        'minimum_user_class',
        'latest_post__author',
        'latest_post__author__user_class',
        'latest_post__thread',
    ).prefetch_related(
        'threads__created_by',
        'threads__latest_post__author',
        'threads__latest_post__author__user_class',
        'threads__latest_post__thread',
    )

    def get_queryset(self):

        queryset = super().get_queryset().accessible_to_user(self.request.user)

        group_id = self.request.query_params.get('group_id', None)
        if group_id is not None:
            queryset = queryset.filter(group_id=group_id)

        return queryset


class ForumThreadViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = ForumThreadSerializer
    queryset = ForumThread.objects.all().select_related(
        'latest_post__author',
        'latest_post__author__user_class',
        'latest_post__thread',
    )

    def get_queryset(self):

        queryset = super().get_queryset().accessible_to_user(self.request.user)

        topic_id = self.request.query_params.get('topic_id', None)
        if topic_id is not None:
            queryset = queryset.filter(topic_id=topic_id)

        return queryset


class ForumPostViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = ForumPostSerializer
    queryset = ForumPost.objects.all().select_related(
        'thread',
        'author',
        'author__user_class',
    )

    def get_queryset(self):

        queryset = super().get_queryset().accessible_to_user(self.request.user)

        thread_id = self.request.query_params.get('thread_id', None)
        if thread_id is not None:
            queryset = queryset.filter(thread_id=thread_id)

        return queryset


class NewsPostViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = ForumPostSerializer

    def get_queryset(self):

        # Earliest post subquery
        earliest_post = ForumPost.objects.filter(
            thread=OuterRef('id'),
        ).order_by(
            'created_at',
        ).values('id')[:1]

        # Get news threads with earliest post
        news_threads = ForumThread.objects.filter(
            topic__name='Announcements',
        ).annotate(
            earliest_post_id=Subquery(earliest_post),
        )

        # Return earliest posts from each thread
        return ForumPost.objects.filter(
            id__in=news_threads.values('earliest_post_id'),
        ).select_related(
            'thread',
            'author',
            'author__user_class',
        ).order_by(
            '-created_at',
        )

    def get_object(self):
        """
        If the 'latest' identifier is requested, fetch the most recent news post.
        """
        if self.action == 'retrieve' and self.kwargs[self.lookup_field] == 'latest':
            return self.get_queryset().first()
        return super().get_object()


def forum_index(request):

    forum_topics = ForumTopic.objects.accessible_to_user(request.user).select_related(
        'group',
    ).order_by(
        'group__sort_order',
        'sort_order',
    )

    forum_groups = OrderedDict()
    for topic in forum_topics:
        group_name = topic.group.name
        if group_name in forum_groups:
            forum_groups[group_name].append(topic)
        else:
            forum_groups[group_name] = [topic]

    return render(
        request=request,
        template_name='forum_index.html',
        context={
            'forum_groups': forum_groups,
        }
    )


def forum_topic_details(request, topic_id):

    topic = get_object_or_404(
        ForumTopic.objects.accessible_to_user(request.user),
        id=topic_id,
    )

    threads = paginate(
        request=request,
        queryset=topic.threads.select_related('created_by'),
        items_per_page=25,
    )

    return render(
        request=request,
        template_name='forum_topic_details.html',
        context={
            'topic': topic,
            'threads': threads,
        }
    )


def forum_post_delete(request, post_id):

    post = get_object_or_404(
        ForumPost,
        id=post_id
    )

    thread = post.thread

    post.delete()

    return redirect(thread)


class ForumThreadView(View):

    def dispatch(self, request, *args, **kwargs):

        self.thread = get_object_or_404(
            ForumThread.objects.accessible_to_user(request.user),
            id=kwargs.pop('thread_id'),
        )

        self.posts = paginate(
            request=request,
            queryset=self.thread.posts.select_related('author'),
            items_per_page=25,
        )

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        form = ForumPostForm(
            thread=self.thread,
            author=request.user,
        )

        return self._render(
            thread=self.thread,
            posts=self.posts,
            form=form,
        )

    def post(self, request):

        form = ForumPostForm(
            request.POST,
            thread=self.thread,
            author=request.user,
        )

        if form.is_valid():

            forum_post = form.save()
            return redirect(forum_post)

        else:

            return self._render(
                thread=self.thread,
                posts=self.posts,
                form=form,
            )

    def _render(self, thread, posts, form):
        return render(
            request=self.request,
            template_name='forum_thread_details.html',
            context={
                'thread': thread,
                'posts': posts,
                'form': form,
            },
        )
