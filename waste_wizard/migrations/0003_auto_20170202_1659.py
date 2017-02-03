# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste_wizard', '0002_auto_20170202_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wasteitem',
            name='description',
            field=models.CharField(max_length=200, verbose_name='Waste item description', db_index=True),
        ),
    ]
