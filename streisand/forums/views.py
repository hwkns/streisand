# -*- coding: utf-8 -*-

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django_filters import rest_framework as filters
from rest_framework import mixins
from collections import OrderedDict
from rest_framework.mixins import Response
from django.db.models import OuterRef, Subquery
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from www.utils import paginate
from www.pagination import ForumsPageNumberPagination
from .forms import ForumPostForm
from .models import ForumGroup, ForumTopic, ForumThread, ForumPost, ForumThreadSubscription
from .serializers import (
    ForumGroupSerializer,
    ForumTopicSerializer,
    ForumThreadSerializer,
    ForumPostSerializer,
    ForumThreadIndexSerializer,
    ForumThreadSubscriptionSerializer,
)
from .filters import ForumTopicFilter, ForumThreadFilter, ForumPostFilter


class ForumGroupViewSet(ModelViewSet):
    """
    API endpoint that allows ForumGroups to be viewed, edited, or created.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ForumGroupSerializer
    queryset = ForumGroup.objects.all().prefetch_related(
        'topics__latest_post__author',
        'topics__latest_post__author__user_class',
        'topics__latest_post__thread',
    ).order_by('sort_order').distinct('sort_order')
    pagination_class = ForumsPageNumberPagination

    def get_queryset(self):
        return super().get_queryset().accessible_to_user(self.request.user)


class ForumTopicViewSet(ModelViewSet):
    """
    API endpoint that allows ForumTopics to be created, viewed, edited, or deleted.
    Please Note: Pagination is set to Page Number Pagination.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ForumTopicSerializer
    queryset = ForumTopic.objects.all().select_related(
        'group', 'minimum_user_class', 'latest_post'
    ).prefetch_related(
        'group', 'minimum_user_class', 'threads',
        'latest_post', 'latest_post__author',
        'latest_post__author__user_class',
        'latest_post__thread__topic'
    ).order_by('sort_order').distinct('sort_order')
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ForumTopicFilter
    pagination_class = ForumsPageNumberPagination

    def get_queryset(self):

        queryset = super().get_queryset().accessible_to_user(self.request.user)

        group_id = self.request.query_params.get('group_id', None)
        if group_id is not None:
            queryset = queryset.filter(group_id=group_id)

        return queryset


class ForumThreadIndexViewSet(ModelViewSet):
    """
    API endpoint that allows ForumThreads to be viewed, and edited.
    This endpoint does not include all posts, see the forum-threads viewset for a list,
    and forum-thread-items for creating/updating/deleting.
    Please Note: Pagination is set to Page Number Pagination.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ForumThreadIndexSerializer
    queryset = ForumThread.objects.all().prefetch_related(
        'topic__group',
        'created_by',
        'posts__thread',
        'posts__author',
        'latest_post',
        'latest_post__thread_latest',
        'latest_post__author',
        'topic__latest_post__author',
        'topic__latest_post__author__user_class',
        'topic__latest_post__thread',
    ).order_by('-is_sticky', '-latest_post__created_at').distinct('is_sticky', 'latest_post__created_at')
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ForumThreadFilter
    pagination_class = ForumsPageNumberPagination

    def get_queryset(self):

        queryset = super().get_queryset().accessible_to_user(self.request.user)

        topic_id = self.request.query_params.get('topic_id', None)
        if topic_id is not None:
            queryset = queryset.filter(topic_id=topic_id)

        return queryset


class ForumThreadWithAllPostsViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    API endpoint that allows ForumThreads to be viewed only. This view shows all Forum Threads and associated posts.
    Please Note: Pagination is set to Page Number Pagination.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ForumThreadSerializer
    queryset = ForumThread.objects.all().prefetch_related(
        'posts',
        'created_by',
        'posts__thread',
        'posts__author',
        'latest_post',
        'latest_post__thread_latest',
        'latest_post__author',
        'topic__latest_post__author',
        'topic__latest_post__author__user_class',
        'topic__latest_post__thread',
        'subscribed_users',
    ).order_by('-created_at').distinct('created_at')
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ForumThreadFilter
    pagination_class = ForumsPageNumberPagination

    def get_queryset(self):

        queryset = super().get_queryset().accessible_to_user(self.request.user)

        topic_id = self.request.query_params.get('topic_id', None)
        if topic_id is not None:
            queryset = queryset.filter(topic_id=topic_id)

        return queryset


class ForumThreadItemViewSet(mixins.UpdateModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                             mixins.RetrieveModelMixin, GenericViewSet):
    """
    API endpoint that allows ForumThreads to be created, updated, edited or deleted only.
    Please Note: Pagination is set to Page Number Pagination.
    """
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, pk=None):
        serializer = ForumThreadSerializer(request.user, data=request.data, partial=True)
        serializer.save()
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
    serializer_class = ForumThreadSerializer
    queryset = ForumThread.objects.all().prefetch_related(
        'created_by',
        'posts__author',
        'latest_post',
        'latest_post__author',
        'topic__latest_post__author',
        'topic__latest_post__author__user_class',
        'topic__latest_post__thread',
    ).order_by('topic__latest_post__thread').distinct('topic__latest_post__thread')
    pagination_class = ForumsPageNumberPagination

    def get_queryset(self):

        queryset = super().get_queryset().accessible_to_user(self.request.user)

        topic_id = self.request.query_params.get('topic_id', None)
        if topic_id is not None:
            queryset = queryset.filter(topic_id=topic_id)

        return queryset


class ForumPostViewSet(ModelViewSet):
    """
    API endpoint that allows ForumPosts to be created, viewed, edited or deleted.
    Please Note: Pagination is set to Page Number Pagination.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ForumPostSerializer
    queryset = ForumPost.objects.all().prefetch_related(
        'thread',
        'thread__topic',
        'topic_latest__latest_post',
        'author',
        'author__user_class',
    ).order_by('-created_at').distinct('created_at')
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ForumPostFilter
    pagination_class = ForumsPageNumberPagination

    def get_queryset(self):

        queryset = super().get_queryset().accessible_to_user(self.request.user)

        thread_id = self.request.query_params.get('thread_id', None)
        if thread_id is not None:
            queryset = queryset.filter(thread_id=thread_id)

        return queryset


class ForumThreadSubscriptionViewSet(ModelViewSet):

    """
    API endpoint that allows ThreadSubscriptions to be viewed, or edited.
    Please Note: Pagination is set to Page Number Pagination.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ForumThreadSubscriptionSerializer
    queryset = ForumThreadSubscription.objects.all().prefetch_related(
        'thread',
    ).order_by('-thread').distinct('thread')
    pagination_class = ForumsPageNumberPagination


class NewsPostViewSet(ModelViewSet):
    """
    API endpoint that allows LatestForumPosts to be viewed, or edited.
    Please Note: Pagination is set to Page Number Pagination.
    """
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
        ).prefetch_related(
            'thread',
            'author',
            'author__user_class',
        ).order_by(
            '-created_at',
        ).distinct()

    pagination_class = ForumsPageNumberPagination

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
