# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste_schedule', '0011_delete_scheduleexception'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduledetail',
            name='service_type',
            field=models.CharField(verbose_name='Service', default='all', max_length=32, help_text='(comma-delimited combination of any of the following: all, bulk, hazardous, recycling, recycle here, street sweeper, trash, transfer station, yard waste)'),
        ),
    ]
