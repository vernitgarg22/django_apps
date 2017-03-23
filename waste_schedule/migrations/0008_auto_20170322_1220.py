# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import re
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('waste_schedule', '0007_auto_20170322_1218'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('detail_type', models.CharField(verbose_name='Type of information', max_length=128, choices=[('schedule', 'Schedule Change'), ('start-date', 'Service Start Date'), ('end-date', 'Service End Date'), ('info', 'Alert')])),
                ('service_type', models.CharField(verbose_name='Service', max_length=32, choices=[('all', 'All Services'), ('bulk', 'Bulk'), ('hazardous', 'Hazardous Waste'), ('recycling', 'Recycling'), ('recycle here', 'Recycle Here'), ('trash', 'Trash'), ('transfer station', 'Transfer Station'), ('yard waste', 'Yard Waste')], default='all')),
                ('description', models.CharField(verbose_name='Description of change', max_length=256)),
                ('normal_day', models.DateField(verbose_name='Normal day of service', db_index=True, null=True, blank=True)),
                ('new_day', models.DateField(verbose_name='Rescheduled day of service', db_index=True, null=True, blank=True)),
                ('note', models.CharField(verbose_name='Note', max_length=256, null=True, blank=True)),
                ('waste_area_ids', models.CharField(verbose_name='Waste area(s) effected', max_length=1028, null=True, validators=[django.core.validators.RegexValidator(re.compile('^[\\d,]+\\Z', 32), 'Enter only digits separated by commas.', 'invalid')], blank=True)),
            ],
        ),
    ]
