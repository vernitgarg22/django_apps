# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste_schedule', '0006_auto_20170321_1630'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ScheduleDetail',
        ),
    ]
