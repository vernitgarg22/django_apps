# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste_wizard', '0005_auto_20170214_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wasteitem',
            name='destination',
            field=models.CharField(choices=[('bulk', 'Bulk'), ('hazardous', 'Hazardous Waste'), ('recycling', 'Recycling'), ('recycle here', 'Recycle Here'), ('trash', 'Trash'), ('transfer station', 'Transfer Station'), ('yard waste', 'Yard Waste')], verbose_name='Correct destination', max_length=32),
        ),
        migrations.AlterField(
            model_name='wasteitem',
            name='image_url',
            field=models.CharField(choices=[('bulk.png', 'Bulk'), ('recycle_here.jpg', 'Recycle Here'), ('recycling.png', 'Recycling'), ('trash.png', 'Trash'), ('yard_waste.png', 'Yard Waste')], verbose_name='Associated image (optional)', blank=True, default='', max_length=100),
        ),
    ]
