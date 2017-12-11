# -*- coding: utf-8 -*-

from import_scripts.management.commands import MySQLCommand

from forums.models import ForumTopic, ForumThread
from profiles.models import UserProfile
from user_classes.models import UserClass


class Command(MySQLCommand):

    SQL = """
        SELECT * FROM forums_topics
    """

    help = "Imports forum threads from the MySQL db"

    def handle_row(self, row):

        old_id = row['ID']
        title = row['Title']
        author_id = row['AuthorID']
        is_locked = row['IsLocked'] == '1'
        is_sticky = row['IsSticky'] == '1'
        forum_topic_id = row['ForumID']

        try:
            forum_topic = ForumTopic.objects.get(old_id=forum_topic_id)
        except ForumTopic.DoesNotExist:
            print('Forum', forum_topic_id, 'does not exist!')
            forum_topic = ForumTopic.objects.create(
                old_id=forum_topic_id,
                sort_order=0,
                group_id=1,
                name='[DELETED TOPIC]',
                description='',
                minimum_user_class=UserClass.objects.get(name='Developer'),
                staff_only_thread_creation=True,
            )

        try:
            author = UserProfile.objects.get(old_id=author_id)
        except UserProfile.DoesNotExist:
            # print('User', author_id, 'does not exist!!!!!!!!!!!!!!!!!!!!!!!!')
            author = None

        forum_thread = ForumThread.objects.create(
            topic=forum_topic,
            old_id=old_id,
            title=title,
            is_locked=is_locked,
            is_sticky=is_sticky,
            created_by=author,
        )

        print(forum_thread)
