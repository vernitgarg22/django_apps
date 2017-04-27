# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste_wizard', '0007_auto_20170426_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wasteitem',
            name='destination',
            field=models.CharField(verbose_name='Correct destination', max_length=32, choices=[('bulk', 'Bulk'), ('hazardous', 'Hazardous Waste'), ('recycling', 'Recycling'), ('recycle here', 'Recycle Here'), ('street sweeper', 'Street Sweeper'), ('trash', 'Trash'), ('transfer station', 'Transfer Station'), ('yard waste', 'Yard Waste')]),
        ),
    ]
