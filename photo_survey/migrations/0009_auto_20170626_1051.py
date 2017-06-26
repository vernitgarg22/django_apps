# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_survey', '0008_auto_20170625_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemetadata',
            name='common_name',
            field=models.CharField(verbose_name='Common name', null=True, blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='imagemetadata',
            name='house_number',
            field=models.IntegerField(verbose_name='House number', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='imagemetadata',
            name='note',
            field=models.CharField(verbose_name='Image note', null=True, blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='imagemetadata',
            name='street_name',
            field=models.CharField(verbose_name='Street name', null=True, blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='imagemetadata',
            name='street_type',
            field=models.CharField(verbose_name='Street type', null=True, blank=True, max_length=32),
        ),
        migrations.AlterField(
            model_name='imagemetadata',
            name='zipcode',
            field=models.CharField(verbose_name='zipcode', null=True, blank=True, max_length=16),
        ),
    ]
