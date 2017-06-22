# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_survey', '0002_surveydata_surveytemplate'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveytemplate',
            name='user_id',
            field=models.CharField(default='xyz', verbose_name='User ID', db_index=True, max_length=64),
            preserve_default=False,
        ),
    ]
