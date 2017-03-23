# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import re
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('waste_schedule', '0005_auto_20170315_1148'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleDetail',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('change_type', models.CharField(choices=[('schedule', 'Schedule Change'), ('start-date', 'Service Start Date'), ('end-date', 'Service End Date'), ('info', 'Alert')], verbose_name='Type of schedule change', max_length=128)),
                ('description', models.CharField(verbose_name='Description of change', max_length=256)),
                ('normal_day', models.DateField(db_index=True, null=True, verbose_name='Normal day of service')),
                ('new_day', models.DateField(db_index=True, null=True, verbose_name='Rescheduled day of service')),
                ('note', models.CharField(verbose_name='Note', null=True, max_length=256)),
                ('waste_area_ids', models.CharField(verbose_name='Waste area(s) effected', validators=[django.core.validators.RegexValidator(re.compile('^[\\d,]+\\Z', 32), 'Enter only digits separated by commas.', 'invalid')], null=True, max_length=1028)),
            ],
        ),
    ]
