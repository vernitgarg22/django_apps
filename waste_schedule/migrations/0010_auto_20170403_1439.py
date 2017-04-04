# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste_schedule', '0009_auto_20170403_1422'),
    ]

    operations = [
        migrations.DeleteModel(
            name='WasteArea',
        ),
    ]
