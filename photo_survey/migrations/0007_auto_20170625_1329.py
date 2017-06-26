# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_survey', '0006_auto_20170625_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemetadata',
            name='altitude',
            field=models.DecimalField(decimal_places=3, max_digits=6, blank=True),
        ),
        migrations.AlterField(
            model_name='imagemetadata',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, blank=True),
        ),
        migrations.AlterField(
            model_name='imagemetadata',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, blank=True),
        ),
    ]
