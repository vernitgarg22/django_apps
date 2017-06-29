# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_survey', '0017_auto_20170627_1612'),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('survey_template_id', models.CharField(verbose_name='Survey name or ID', db_index=True, max_length=32)),
                ('user_id', models.CharField(verbose_name='User ID', db_index=True, max_length=64)),
                ('parcel_id', models.CharField(verbose_name='Parcel id', db_index=True, max_length=32)),
                ('common_name', models.CharField(verbose_name='Parcel common name', max_length=1024)),
                ('note', models.CharField(verbose_name='Note', max_length=1024)),
                ('status', models.CharField(verbose_name='Survey status', blank=True, db_index=True, max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='SurveyAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('survey_template_id', models.CharField(verbose_name='Survey name or ID', db_index=True, max_length=32)),
                ('question_id', models.CharField(verbose_name='Question identifier', max_length=64)),
                ('answer', models.CharField(verbose_name='Answer', max_length=1024)),
                ('note', models.CharField(verbose_name='Note', blank=True, max_length=1024)),
            ],
        ),
        migrations.RenameModel(
            old_name='SurveyTemplate',
            new_name='SurveyQuestion',
        ),
        migrations.DeleteModel(
            name='SurveyData',
        ),
        migrations.DeleteModel(
            name='TestModel',
        ),
        migrations.AddField(
            model_name='imagemetadata',
            name='altitude',
            field=models.FloatField(default=0, verbose_name='Image altitude'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='imagemetadata',
            name='latitude',
            field=models.FloatField(default=0, verbose_name='Image latitude'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='imagemetadata',
            name='longitude',
            field=models.FloatField(default=0, verbose_name='Image longitude'),
            preserve_default=False,
        ),
    ]
