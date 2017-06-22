# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_survey', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyData',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('survey_template_id', models.CharField(db_index=True, verbose_name='Survey name or ID', max_length=32)),
                ('question_id', models.CharField(verbose_name='Question identifier', max_length=64)),
                ('answer', models.CharField(verbose_name='Answer', max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='SurveyTemplate',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('survey_template_id', models.CharField(db_index=True, verbose_name='Survey name or ID', max_length=32)),
                ('question_id', models.CharField(verbose_name='Question identifier', max_length=64)),
                ('question_number', models.PositiveIntegerField(verbose_name='Question number')),
                ('question_text', models.CharField(help_text='The actual human-readable question itself', verbose_name='Question', max_length=256)),
                ('valid_answers', models.CharField(help_text="Pipe-delimited list of valid answers ('*' = anything)", verbose_name='Valid answers', max_length=256)),
            ],
        ),
    ]
