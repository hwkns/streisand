# -*- coding: utf-8 -*-

from collections import OrderedDict

from django.shortcuts import render, get_object_or_404

from www.utils import paginate

from .models import ForumTopic, ForumThread


def forum_index(request):

    forum_topics = ForumTopic.objects.accessible_to_user(request.user).select_related(
        'group',
    ).order_by(
        'group__sort_order',
        'sort_order',
    )

    forum_groups = OrderedDict()
    for topic in forum_topics:
        if topic.group.name in forum_groups:
            forum_groups[topic.group.name].append(topic)
        else:
            forum_groups[topic.group.name] = [topic]

    return render(
        request=request,
        template_name='forum_index.html',
        dictionary={
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
        queryset=topic.threads.select_related(
            'created_by__user',
        ),
        items_per_page=25,
    )

    return render(
        request=request,
        template_name='forum_topic_details.html',
        dictionary={
            'topic': topic,
            'threads': threads,
        }
    )


def forum_thread_details(request, thread_id):

    thread = get_object_or_404(
        ForumThread.objects.accessible_to_user(request.user),
        id=thread_id
    )

    posts = paginate(
        request=request,
        queryset=thread.posts.select_related(
            'author__user',
        ),
        items_per_page=25,
    )

    return render(
        request=request,
        template_name='forum_thread_details.html',
        dictionary={
            'thread': thread,
            'posts': posts,
        }
    )
