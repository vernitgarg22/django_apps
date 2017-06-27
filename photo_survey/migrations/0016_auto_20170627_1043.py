# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_survey', '0015_testmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='testmodel',
            name='altitude',
            field=models.DecimalField(decimal_places=3, max_digits=8, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testmodel',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=10, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testmodel',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=10, default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='testmodel',
            name='decimal',
            field=models.DecimalField(decimal_places=6, max_digits=10),
        ),
    ]
