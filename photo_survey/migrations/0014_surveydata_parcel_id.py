# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_survey', '0013_auto_20170626_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveydata',
            name='parcel_id',
            field=models.CharField(max_length=32, db_index=True, verbose_name='Path to image file', default='xyz'),
            preserve_default=False,
        ),
    ]
