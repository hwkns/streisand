# Generated by Django 2.0.4 on 2018-04-17 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('torrent_stats', '0001_initial'),
        ('torrents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='torrentstats',
            name='torrent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='torrent_stats', to='torrents.Torrent'),
        ),
    ]
