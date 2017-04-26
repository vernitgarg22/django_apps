# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste_wizard', '0006_auto_20170313_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wasteitem',
            name='image_url',
            field=models.CharField(choices=[('bulk.png', 'Bulk'), ('recycle_here.jpg', 'Recycle Here'), ('recycling.png', 'Recycling'), ('trash.png', 'Trash'), ('yard_waste.jpg', 'Yard Waste')], blank=True, max_length=100, verbose_name='Associated image (optional)', default=''),
        ),
    ]
