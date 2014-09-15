# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Peer',
            fields=[
                ('id', django_extensions.db.fields.UUIDField(serialize=False, primary_key=True, blank=True, name='id', editable=False)),
                ('user_auth_key', models.CharField(max_length=36)),
                ('peer_id', models.CharField(max_length=40)),
                ('ip_address', models.GenericIPAddressField()),
                ('port', models.CharField(max_length=5)),
                ('bytes_uploaded', models.BigIntegerField(default=0)),
                ('bytes_downloaded', models.BigIntegerField(default=0)),
                ('complete', models.BooleanField(default=False)),
                ('first_announce', models.DateTimeField(auto_now_add=True)),
                ('last_announce', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Swarm',
            fields=[
                ('torrent_info_hash', models.CharField(primary_key=True, serialize=False, max_length=40)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='peer',
            name='swarm',
            field=models.ForeignKey(to='tracker.Swarm', related_name='peers'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='peer',
            unique_together=set([('swarm', 'user_auth_key', 'ip_address', 'port')]),
        ),
    ]
