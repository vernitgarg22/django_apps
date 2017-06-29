# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_survey', '0018_auto_20170629_1427'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='surveyanswer',
            name='survey_template_id',
        ),
        migrations.AddField(
            model_name='surveyanswer',
            name='survey',
            field=models.ForeignKey(to='photo_survey.Survey', default=1),
            preserve_default=False,
        ),
    ]
