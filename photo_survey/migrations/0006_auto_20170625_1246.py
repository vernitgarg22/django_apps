# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_survey', '0005_auto_20170625_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagemetadata',
            name='common_name',
            field=models.CharField(max_length=128, verbose_name='Common name', blank=True),
        ),
        migrations.AddField(
            model_name='imagemetadata',
            name='house_number',
            field=models.IntegerField(verbose_name='House number', blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='imagemetadata',
            name='street_name',
            field=models.CharField(max_length=128, verbose_name='Street name', blank=True),
        ),
        migrations.AddField(
            model_name='imagemetadata',
            name='street_type',
            field=models.CharField(max_length=32, verbose_name='Street type', blank=True),
        ),
        migrations.AddField(
            model_name='imagemetadata',
            name='zipcode',
            field=models.CharField(max_length=16, verbose_name='zipcode', blank=True),
        ),
        migrations.AlterField(
            model_name='imagemetadata',
            name='created_at',
            field=models.DateTimeField(verbose_name='Time when image was created'),
        ),
    ]
