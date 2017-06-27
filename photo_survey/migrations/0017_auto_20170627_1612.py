# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_survey', '0016_auto_20170627_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testmodel',
            name='altitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='testmodel',
            name='decimal',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='testmodel',
            name='latitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='testmodel',
            name='longitude',
            field=models.FloatField(),
        ),
    ]
