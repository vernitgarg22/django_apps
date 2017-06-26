# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_survey', '0004_auto_20170622_1818'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagemetadata',
            name='altitude',
            field=models.DecimalField(max_digits=6, default=0, decimal_places=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='imagemetadata',
            name='latitude',
            field=models.DecimalField(max_digits=9, default=0, decimal_places=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='imagemetadata',
            name='longitude',
            field=models.DecimalField(max_digits=9, default=0, decimal_places=6),
            preserve_default=False,
        ),
    ]
