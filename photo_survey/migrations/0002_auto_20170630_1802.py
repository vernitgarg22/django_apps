# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_survey', '0001_squashed_0019_auto_20170629_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='image_url',
            field=models.CharField(verbose_name='Image used for survey', default='', max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='imagemetadata',
            name='altitude',
            field=models.FloatField(verbose_name='Image altitude'),
        ),
        migrations.AlterField(
            model_name='imagemetadata',
            name='latitude',
            field=models.FloatField(verbose_name='Image latitude'),
        ),
        migrations.AlterField(
            model_name='imagemetadata',
            name='longitude',
            field=models.FloatField(verbose_name='Image longitude'),
        ),
        migrations.AlterField(
            model_name='surveyanswer',
            name='survey',
            field=models.ForeignKey(to='photo_survey.Survey'),
        ),
    ]
