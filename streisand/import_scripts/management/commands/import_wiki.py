# -*- coding: utf-8 -*-

from pytz import UTC

from import_scripts.management.commands import MySQLCommand

from wiki.models import WikiArticle
from profiles.models import UserProfile
from user_classes.models import UserClass


class Command(MySQLCommand):

    SQL = """
        SELECT * FROM wiki_articles
    """

    help = "Imports wiki articles from the MySQL db"

    def handle_row(self, row):

        old_id = row['ID']
        author_id = row['Author']
        title = row['Title']
        body = row['Body']
        modified_at = row['Date']

        try:
            modified_by = UserProfile.objects.get(old_id=author_id)
        except UserProfile.DoesNotExist:
            # print('User', author_id, 'does not exist!!!!!!!!!!!!!!!!!!!!!!!!')
            modified_by = None

        article = WikiArticle.objects.create(
            old_id=old_id,
            title=title,
            body=body.encode('latin-1').decode('utf-8'),
            modified_by=modified_by,
            read_access_minimum_user_class=self.moderator_user_class,
            write_access_minimum_user_class=self.moderator_user_class,
        )

        WikiArticle.objects.filter(id=article.id).update(modified_at=modified_at.replace(tzinfo=UTC))

    def pre_sql(self):
        print('importing wiki articles...')
        self.moderator_user_class = UserClass.objects.get(name='Moderator')

    def post_sql(self):
        print('finished importing wiki articles')
