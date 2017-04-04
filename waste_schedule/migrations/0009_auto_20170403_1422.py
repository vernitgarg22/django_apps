# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste_schedule', '0008_auto_20170322_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduledetail',
            name='detail_type',
            field=models.CharField(max_length=128, choices=[('schedule', 'Schedule Change'), ('start-date', 'Service Start Date'), ('end-date', 'Service End Date'), ('info', 'Notification')], verbose_name='Type of information'),
        ),
        migrations.AlterField(
            model_name='scheduledetail',
            name='service_type',
            field=models.CharField(max_length=32, help_text='(comma-delimited combination of any of the following: all, bulk, hazardous, recycling, recycle here, trash, transfer station, yard waste)', verbose_name='Service', default='all'),
        ),
        migrations.DeleteModel(
            name='ScheduleChange',
        ),
    ]
