# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_survey', '0009_auto_20170626_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveytemplate',
            name='required_by',
            field=models.CharField(help_text='Question / Answer pair that makes this required', blank=True, max_length=64, null=True, verbose_name='Required by'),
        ),
        migrations.AddField(
            model_name='surveytemplate',
            name='required_by_answer',
            field=models.CharField(help_text='Specific Answer pattern that makes this required', blank=True, max_length=64, null=True, verbose_name='Required by answer'),
        ),
    ]
