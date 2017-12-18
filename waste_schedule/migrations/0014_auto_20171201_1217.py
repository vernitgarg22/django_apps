# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-01 17:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste_schedule', '0013_auto_20170724_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduledetail',
            name='description',
            field=models.CharField(max_length=512, verbose_name='Description of change'),
        ),
        migrations.AlterField(
            model_name='scheduledetail',
            name='waste_area_ids',
            field=models.CharField(blank=True, max_length=1028, null=True, verbose_name='Waste area(s) effected'),
        ),
    ]