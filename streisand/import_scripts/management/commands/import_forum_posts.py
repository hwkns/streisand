# -*- coding: utf-8 -*-

from pytz import UTC

from import_scripts.management.commands import MySQLCommand

from forums.models import ForumThread
from profiles.models import UserProfile


class Command(MySQLCommand):

    SQL = """
        SELECT * FROM forums_posts
    """

    help = "Imports forum posts from the MySQL db"

    def handle_row(self, row):

        old_id = row['ID']
        author_id = row['AuthorID']
        body = row['Body']
        created_at = row['AddedTime']
        modified_at = row['EditedTime']
        # modified_by = row['EditedUserID']

        forum_thread = ForumThread.objects.get(old_id=row['TopicID'])

        try:
            author = UserProfile.objects.get(old_id=author_id)
        except UserProfile.DoesNotExist:
            # print('User', author_id, 'does not exist!!!!!!!!!!!!!!!!!!!!!!!!')
            author = None

        forum_post = forum_thread.posts.create(
            old_id=old_id,
            body=body.encode('latin-1').decode('utf-8'),
            author=author,
        )

        forum_post.created_at = created_at.replace(tzinfo=UTC)
        if modified_at:
            forum_post.modified_at = modified_at.replace(tzinfo=UTC)
        else:
            forum_post.modified_at = forum_post.created_at
        forum_post.save()

    def pre_sql(self):
        print('importing forum posts...')

    def post_sql(self):
        print('finished importing forum posts')
