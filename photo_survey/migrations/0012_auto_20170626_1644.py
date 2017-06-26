# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_survey', '0011_auto_20170626_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveytemplate',
            name='answer_trigger',
            field=models.CharField(blank=True, help_text="Required action for a given answer. e.g., 'n'", verbose_name='Answer trigger', default='', max_length=16),
        ),
    ]
