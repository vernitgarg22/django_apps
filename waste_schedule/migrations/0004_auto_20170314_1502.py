# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('waste_schedule', '0003_auto_20170313_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedulechange',
            name='waste_area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='waste_schedule.WasteArea'),
        ),
    ]
