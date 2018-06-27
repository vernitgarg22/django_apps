# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste_schedule', '0002_auto_20170214_2007'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleChange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('service_type', models.CharField(default='all', choices=[('all', 'All Services'), ('bulk', 'Bulk'), ('hazardous', 'Hazardous Waste'), ('recycling', 'Recycling'), ('recycle here', 'Recycle Here'), ('trash', 'Trash'), ('transfer station', 'Transfer Station'), ('yard waste', 'Yard Waste')], verbose_name='Service', max_length=32)),
                ('normal_day', models.DateField(db_index=True, verbose_name='Normal day of service')),
                ('rescheduled_day', models.DateField(db_index=True, verbose_name='New day of service')),
                ('reason', models.CharField(verbose_name='Reason for change', blank=True, max_length=300)),
                ('note', models.CharField(verbose_name='Special note for residents', blank=True, max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='WasteArea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(db_index=True, verbose_name='Waste area description', unique=True, max_length=128)),
            ],
        ),
        migrations.AddField(
            model_name='schedulechange',
            name='waste_area',
            field=models.ForeignKey(to='waste_schedule.WasteArea', on_delete=models.PROTECT),
        ),
    ]
