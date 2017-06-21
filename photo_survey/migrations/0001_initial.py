# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('file_path', models.CharField(verbose_name='Path to image file', max_length=256, db_index=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ImageMetadata',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('parcel_id', models.CharField(verbose_name='Path to image file', max_length=32, db_index=True)),
                ('created_at', models.DateTimeField(verbose_name='Time when image was added')),
                ('note', models.CharField(verbose_name='Image note', max_length=128, blank=True)),
                ('image', models.ForeignKey(to='photo_survey.Image')),
            ],
        ),
    ]
