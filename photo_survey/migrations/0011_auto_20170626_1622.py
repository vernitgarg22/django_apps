# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_survey', '0010_auto_20170626_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveytemplate',
            name='answer_trigger',
            field=models.CharField(verbose_name='Answer trigger', max_length=16, help_text="Required action for a given result. e.g., 'n'", blank=True, default=''),
        ),
        migrations.AddField(
            model_name='surveytemplate',
            name='answer_trigger_result',
            field=models.CharField(verbose_name='Trigger action', max_length=16, help_text="Action to take if a trigger goes off. e.g., 'stop'", blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='surveytemplate',
            name='required_by',
            field=models.CharField(verbose_name='Required by', max_length=64, help_text="Question / Answer pair that makes answer required. 'n' makes answer optional. Default is required", blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='surveytemplate',
            name='required_by_answer',
            field=models.CharField(verbose_name='Required by answer', max_length=64, help_text='Specific answer pattern that makes this required', blank=True, default=''),
        ),
    ]
