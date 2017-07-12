# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_survey', '0003_survey_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyQuestionAvailAnswer',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('value', models.CharField(help_text='Answer value as stored in database', max_length=64, verbose_name='Answer Value')),
                ('text', models.CharField(help_text='Human-readable version of answer', max_length=128, verbose_name='Human-readable Answer')),
                ('survey_question', models.ForeignKey(to='photo_survey.SurveyQuestion')),
            ],
        ),
    ]
