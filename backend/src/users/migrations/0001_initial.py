# Generated by Django 2.0.6 on 2018-06-04 13:22

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('torrent_stats', '0002_torrentstats_torrent'),
        ('auth', '0009_alter_user_last_name_max_length'),
        ('torrents', '0001_initial'),
        ('films', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_banned', models.BooleanField(default=False)),
                ('old_id', models.PositiveIntegerField(db_index=True, null=True)),
                ('is_donor', models.BooleanField(default=False)),
                ('account_status', models.CharField(choices=[('unconfirmed', 'Unconfirmed'), ('enabled', 'Enabled'), ('disabled', 'Disabled')], db_index=True, default='enabled', max_length=32)),
                ('failed_login_attempts', models.PositiveIntegerField(default=0)),
                ('avatar_url', models.URLField(blank=True, max_length=512, null=True)),
                ('custom_title', models.CharField(blank=True, max_length=256, null=True)),
                ('profile_description', models.TextField(blank=True, null=True)),
                ('staff_notes', models.TextField(null=True)),
                ('irc_key', models.CharField(blank=True, max_length=128, null=True)),
                ('invite_count', models.PositiveIntegerField(default=0)),
                ('bytes_uploaded', models.BigIntegerField(default=0)),
                ('bytes_downloaded', models.BigIntegerField(default=0)),
                ('log_successful_announces', models.BooleanField(default=False, help_text="Use sparingly! This logs data from all successful announces made by this user's torrent client(s).")),
                ('last_seeded', models.DateTimeField(null=True)),
                ('average_seeding_size', models.BigIntegerField(default=0)),
            ],
            options={
                'permissions': (('can_invite', 'Can invite new users'), ('unlimited_invites', 'Can invite unlimited new users'), ('custom_title', 'Can edit own custom title')),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserAnnounce',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('time_stamp', models.DateTimeField()),
                ('announce_key', models.UUIDField()),
                ('ip_address', models.GenericIPAddressField()),
                ('port', models.IntegerField()),
                ('peer_id', models.CharField(max_length=40)),
                ('user_agent', models.TextField()),
                ('new_bytes_uploaded', models.BigIntegerField(default=0)),
                ('new_bytes_downloaded', models.BigIntegerField(default=0)),
                ('bytes_remaining', models.BigIntegerField()),
                ('event', models.CharField(max_length=16)),
                ('torrent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='torrents.TorrentFile', to_field='info_hash')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logged_announces', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserAnnounceKey',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('issued_at', models.DateTimeField(auto_now_add=True)),
                ('revoked_at', models.DateTimeField(null=True)),
                ('revocation_notes', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='announce_keys', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_id', models.PositiveIntegerField(db_index=True, null=True)),
                ('name', models.CharField(db_index=True, max_length=128)),
                ('rank', models.PositiveSmallIntegerField(db_index=True)),
                ('is_staff', models.BooleanField(db_index=True, default=False)),
                ('permissions', models.ManyToManyField(blank=True, related_name='user_classes', to='auth.Permission')),
            ],
            options={
                'ordering': ['rank'],
            },
        ),
        migrations.CreateModel(
            name='UserEmailAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_used', models.DateTimeField(auto_now_add=True)),
                ('last_used', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='email_addresses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserIPAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField()),
                ('used_with', models.CharField(max_length=16)),
                ('first_used', models.DateTimeField(auto_now_add=True)),
                ('last_used', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ip_addresses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'last_used',
            },
        ),
        migrations.CreateModel(
            name='UserTorrentDownloadKey',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('issued_at', models.DateTimeField(auto_now_add=True)),
                ('revoked_at', models.DateTimeField(null=True)),
                ('revocation_notes', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='torrent_download_keys', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WatchedUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField()),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('last_checked', models.DateTimeField(auto_now=True)),
                ('checked_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='watched_users_checked', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist_entries', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='announce_key',
            field=models.OneToOneField(default=None, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='current_user', to='users.UserAnnounceKey'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='invited_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='torrent_download_key',
            field=models.OneToOneField(default=None, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='current_user', to='users.UserTorrentDownloadKey'),
        ),
        migrations.AddField(
            model_name='user',
            name='torrents',
            field=models.ManyToManyField(related_name='users', through='torrent_stats.TorrentStats', to='torrents.TorrentFile'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_class',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='users.UserClass'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='user',
            name='watch_queue',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='films.Collection'),
        ),
        migrations.AlterUniqueTogether(
            name='useripaddress',
            unique_together={('user', 'ip_address', 'used_with')},
        ),
        migrations.AlterIndexTogether(
            name='useripaddress',
            index_together={('user', 'ip_address', 'used_with')},
        ),
    ]
