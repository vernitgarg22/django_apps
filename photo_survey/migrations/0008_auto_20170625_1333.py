# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_survey', '0007_auto_20170625_1329'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagemetadata',
            name='altitude',
        ),
        migrations.RemoveField(
            model_name='imagemetadata',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='imagemetadata',
            name='longitude',
        ),
    ]
