# Generated by Django 2.0.4 on 2018-04-17 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Codec',
            fields=[
                ('name', models.CharField(max_length=64, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Container',
            fields=[
                ('name', models.CharField(max_length=64, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Resolution',
            fields=[
                ('name', models.CharField(max_length=64, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SourceMedia',
            fields=[
                ('name', models.CharField(max_length=64, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
