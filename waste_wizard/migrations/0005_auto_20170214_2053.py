# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste_wizard', '0004_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wasteitem',
            name='description',
            field=models.CharField(max_length=200, db_index=True, unique=True, verbose_name='Waste item description'),
        ),
        migrations.AlterField(
            model_name='wasteitem',
            name='destination',
            field=models.CharField(max_length=32, verbose_name='Correct destination', choices=[('trash', 'Trash'), ('recycling', 'Recycling'), ('bulk', 'Bulk'), ('yard waste', 'Yard Waste'), ('compost', 'Compost')]),
        ),
        migrations.AlterField(
            model_name='wasteitem',
            name='image_url',
            field=models.CharField(max_length=100, verbose_name='Associated image (optional)', blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='wasteitem',
            name='keywords',
            field=models.CharField(max_length=300, verbose_name='Associated keywords (optional)', blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='wasteitem',
            name='notes',
            field=models.CharField(max_length=300, verbose_name='Special details to note (optional)', blank=True),
        ),
    ]
