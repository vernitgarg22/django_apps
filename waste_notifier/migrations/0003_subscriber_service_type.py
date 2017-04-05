# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste_notifier', '0002_auto_20170404_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='service_type',
            field=models.CharField(help_text='(comma-delimited combination of any of the following: all, bulk, hazardous, recycling, recycle here, trash, transfer station, yard waste)', default='all', verbose_name='Service', max_length=32),
        ),
    ]
