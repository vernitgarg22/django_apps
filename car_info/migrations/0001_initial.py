# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import re
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LicensePlateInfo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('plate_num', models.CharField(verbose_name='License plate number', unique=True, db_index=True, max_length=16)),
                ('created_at', models.DateTimeField(verbose_name='Date when plate number first added')),
            ],
        ),
    ]
