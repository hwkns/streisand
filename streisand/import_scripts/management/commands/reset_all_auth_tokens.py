# -*- coding: utf-8 -*-

from rest_framework.authtoken.models import Token
from tqdm import tqdm

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):

        users = User.objects.all()
        Token.objects.all().delete()

        for user in tqdm(users.iterator(), total=users.count(), unit='user'):
            Token.objects.create(user=user)
