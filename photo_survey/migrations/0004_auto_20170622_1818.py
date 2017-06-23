# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_survey', '0003_surveytemplate_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='surveytemplate',
            name='user_id',
        ),
        migrations.AddField(
            model_name='surveydata',
            name='user_id',
            field=models.CharField(verbose_name='User ID', max_length=64, db_index=True, default='xyz'),
            preserve_default=False,
        ),
    ]
