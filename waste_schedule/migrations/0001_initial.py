# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleException',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('service_type', models.CharField(choices=[('trash', 'Trash'), ('recycling', 'Recycling'), ('bulk', 'Bulk'), ('yard waste', 'Yard Waste'), ('compost', 'Compost')], max_length=32, verbose_name='Service type')),
                ('normal_day', models.DateField(verbose_name='Normal day of service', db_index=True)),
                ('rescheduled_day', models.DateField(verbose_name='New day of service', db_index=True)),
                ('reason', models.CharField(max_length=300, verbose_name='Reason for change')),
                ('note', models.CharField(max_length=300, verbose_name='Special note for residents')),
            ],
        ),
    ]
