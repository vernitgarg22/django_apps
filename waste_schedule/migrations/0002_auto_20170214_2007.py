# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste_schedule', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduleexception',
            name='note',
            field=models.CharField(verbose_name='Special note for residents', blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='scheduleexception',
            name='reason',
            field=models.CharField(verbose_name='Reason for change', blank=True, max_length=300),
        ),
    ]
