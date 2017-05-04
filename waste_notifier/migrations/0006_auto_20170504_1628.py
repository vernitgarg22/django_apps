# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste_notifier', '0005_auto_20170503_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='address',
            field=models.CharField(max_length=128, null=True, blank=True, verbose_name='Home address'),
        ),
        migrations.AddField(
            model_name='subscriber',
            name='latitude',
            field=models.CharField(max_length=32, null=True, blank=True, verbose_name='Latitude'),
        ),
        migrations.AddField(
            model_name='subscriber',
            name='longitude',
            field=models.CharField(max_length=32, null=True, blank=True, verbose_name='Longitude'),
        ),
    ]
