# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste_wizard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wasteitem',
            name='destination',
            field=models.CharField(verbose_name='Appropriate waste destination', max_length=32, choices=[('trash', 'Trash'), ('recycling', 'Recycling'), ('bulk', 'Bulk'), ('yard waste', 'Yard Waste'), ('compost', 'Compost')]),
        ),
        migrations.AlterField(
            model_name='wasteitem',
            name='keywords',
            field=models.CharField(blank=True, verbose_name='Keywords associated with the item', default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='wasteitem',
            name='notes',
            field=models.CharField(verbose_name='Special details to note', blank=True, max_length=300),
        ),
    ]
