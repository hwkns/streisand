# Generated by Django 2.0.4 on 2018-04-17 15:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('email', models.EmailField(max_length=254, unique=True)),
                ('key', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('offered_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invites', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
