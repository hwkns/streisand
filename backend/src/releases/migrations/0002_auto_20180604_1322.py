# Generated by Django 2.0.6 on 2018-06-04 13:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('releases', '0001_initial'),
        ('media_formats', '0001_initial'),
        ('mediainfo', '0001_initial'),
        ('films', '0002_auto_20180604_1322'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='releasecomment',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='releasecomments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='releasecomment',
            name='release',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='releases.Release'),
        ),
        migrations.AddField(
            model_name='release',
            name='codec',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='torrents', to='media_formats.Codec'),
        ),
        migrations.AddField(
            model_name='release',
            name='container',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='torrents', to='media_formats.Container'),
        ),
        migrations.AddField(
            model_name='release',
            name='encoded_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='encoded_releases', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='release',
            name='film',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='releases', to='films.Film'),
        ),
        migrations.AddField(
            model_name='release',
            name='mediainfo',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='mediainfo.Mediainfo'),
        ),
        migrations.AddField(
            model_name='release',
            name='resolution',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='torrents', to='media_formats.Resolution'),
        ),
        migrations.AddField(
            model_name='release',
            name='source_media',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='torrents', to='media_formats.SourceMedia'),
        ),
    ]
