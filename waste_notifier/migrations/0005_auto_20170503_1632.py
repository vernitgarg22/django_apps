# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste_notifier', '0004_auto_20170412_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='created_at',
            field=models.DateTimeField(blank=True, verbose_name='Time of initial subscription', null=True),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='service_type',
            field=models.CharField(max_length=32, default='all', verbose_name='Service', help_text='(comma-delimited combination of any of the following: all, bulk, hazardous, recycling, recycle here, street sweeper, trash, transfer station, yard waste)'),
        ),
    ]
