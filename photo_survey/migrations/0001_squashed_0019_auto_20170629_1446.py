# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('photo_survey', '0001_initial'), ('photo_survey', '0002_surveydata_surveytemplate'), ('photo_survey', '0003_surveytemplate_user_id'), ('photo_survey', '0004_auto_20170622_1818'), ('photo_survey', '0005_auto_20170625_1231'), ('photo_survey', '0006_auto_20170625_1246'), ('photo_survey', '0007_auto_20170625_1329'), ('photo_survey', '0008_auto_20170625_1333'), ('photo_survey', '0009_auto_20170626_1051'), ('photo_survey', '0010_auto_20170626_1533'), ('photo_survey', '0011_auto_20170626_1622'), ('photo_survey', '0012_auto_20170626_1644'), ('photo_survey', '0013_auto_20170626_1647'), ('photo_survey', '0014_surveydata_parcel_id'), ('photo_survey', '0015_testmodel'), ('photo_survey', '0016_auto_20170627_1043'), ('photo_survey', '0017_auto_20170627_1612'), ('photo_survey', '0018_auto_20170629_1427'), ('photo_survey', '0019_auto_20170629_1446')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('file_path', models.CharField(max_length=256, unique=True, verbose_name='Path to image file', db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='ImageMetadata',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('parcel_id', models.CharField(max_length=32, verbose_name='Path to image file', db_index=True)),
                ('created_at', models.DateTimeField(verbose_name='Time when image was created')),
                ('note', models.CharField(max_length=128, verbose_name='Image note', null=True, blank=True)),
                ('image', models.ForeignKey(to='photo_survey.Image')),
                ('common_name', models.CharField(max_length=128, verbose_name='Common name', null=True, blank=True)),
                ('house_number', models.IntegerField(verbose_name='House number', null=True, blank=True)),
                ('street_name', models.CharField(max_length=128, verbose_name='Street name', null=True, blank=True)),
                ('street_type', models.CharField(max_length=32, verbose_name='Street type', null=True, blank=True)),
                ('zipcode', models.CharField(max_length=16, verbose_name='zipcode', null=True, blank=True)),
                ('altitude', models.FloatField(default=0, verbose_name='Image altitude')),
                ('latitude', models.FloatField(default=0, verbose_name='Image latitude')),
                ('longitude', models.FloatField(default=0, verbose_name='Image longitude')),
            ],
        ),
        migrations.CreateModel(
            name='SurveyQuestion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('survey_template_id', models.CharField(max_length=32, verbose_name='Survey name or ID', db_index=True)),
                ('question_id', models.CharField(max_length=64, verbose_name='Question identifier')),
                ('question_number', models.PositiveIntegerField(verbose_name='Question number')),
                ('question_text', models.CharField(max_length=256, help_text='The actual human-readable question itself', verbose_name='Question')),
                ('valid_answers', models.CharField(max_length=256, help_text="Pipe-delimited list of valid answers ('*' = anything)", verbose_name='Valid answers')),
                ('required_by', models.CharField(max_length=64, help_text="Question / Answer pair that makes answer required. 'n' makes answer optional. Default is required", verbose_name='Required by', blank=True, default='')),
                ('required_by_answer', models.CharField(max_length=64, help_text='Specific answer pattern that makes this required', verbose_name='Required by answer', blank=True, default='')),
                ('answer_trigger', models.CharField(max_length=16, help_text="Required action for a given answer. e.g., 'n'", verbose_name='Answer trigger', blank=True, default='')),
                ('answer_trigger_action', models.CharField(max_length=16, help_text="Action to take if a trigger goes off. e.g., 'stop'", verbose_name='Trigger action', blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('survey_template_id', models.CharField(max_length=32, verbose_name='Survey name or ID', db_index=True)),
                ('user_id', models.CharField(max_length=64, verbose_name='User ID', db_index=True)),
                ('parcel_id', models.CharField(max_length=32, verbose_name='Parcel id', db_index=True)),
                ('common_name', models.CharField(max_length=1024, verbose_name='Parcel common name')),
                ('note', models.CharField(max_length=1024, verbose_name='Note')),
                ('status', models.CharField(max_length=16, verbose_name='Survey status', db_index=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SurveyAnswer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('question_id', models.CharField(max_length=64, verbose_name='Question identifier')),
                ('answer', models.CharField(max_length=1024, verbose_name='Answer')),
                ('note', models.CharField(max_length=1024, verbose_name='Note', blank=True)),
                ('survey', models.ForeignKey(default=1, to='photo_survey.Survey')),
            ],
        ),
    ]
