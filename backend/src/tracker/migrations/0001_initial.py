# Generated by Django 2.0.4 on 2018-05-04 04:33

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Peer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user_announce_key', models.CharField(db_index=True, max_length=36)),
                ('ip_address', models.GenericIPAddressField()),
                ('port', models.IntegerField()),
                ('peer_id', models.CharField(max_length=40)),
                ('user_agent', models.TextField()),
                ('compact_bytes_repr', models.BinaryField(help_text='The compact representation of this peer, sent as bytes to announcing torrent clients')),
                ('bytes_uploaded', models.BigIntegerField(default=0)),
                ('bytes_downloaded', models.BigIntegerField(default=0)),
                ('bytes_remaining', models.BigIntegerField()),
                ('complete', models.BooleanField(default=False)),
                ('first_announce', models.DateTimeField(auto_now_add=True)),
                ('last_announce', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Swarm',
            fields=[
                ('torrent_info_hash', models.CharField(max_length=40, primary_key=True, serialize=False)),
            ],
            options={
                'permissions': (('can_leech', 'Can receive peer lists from the tracker'),),
            },
        ),
        migrations.CreateModel(
            name='TorrentClient',
            fields=[
                ('peer_id_prefix', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('is_whitelisted', models.NullBooleanField(db_index=True)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='peer',
            name='swarm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='peers', to='tracker.Swarm'),
        ),
        migrations.AlterUniqueTogether(
            name='peer',
            unique_together={('swarm', 'user_announce_key', 'ip_address', 'port', 'peer_id')},
        ),
        migrations.AlterIndexTogether(
            name='peer',
            index_together={('swarm', 'user_announce_key', 'ip_address', 'port', 'peer_id')},
        ),
    ]
