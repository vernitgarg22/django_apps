# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-09-05 14:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0002_auto_20190829_1018'),
    ]

    operations = [
        migrations.AddField(
            model_name='messengerlocation',
            name='prefix',
            field=models.CharField(default='citywide', max_length=16, verbose_name='Prefix'),
        ),
        migrations.AlterField(
            model_name='messengerlocation',
            name='location_type',
            field=models.CharField(choices=[('DHSEM Evacuation Zone', 'DHSEM Evacuation Zone'), ('ZIP Code', 'ZIP Code')], max_length=32, verbose_name='Location Type'),
        ),
        migrations.AlterField(
            model_name='messengernotification',
            name='formatter',
            field=models.CharField(blank=True, choices=[('DHSEMFormatter', 'DHSEMFormatter'), ('ElectionFormatter', 'ElectionFormatter')], max_length=64, null=True, verbose_name='Formatter class to render message'),
        ),
        migrations.AlterField(
            model_name='messengersubscriber',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 5, 14, 54, 16, 421583, tzinfo=utc), verbose_name='Time of initial subscription'),
        ),
        migrations.AlterField(
            model_name='messengersubscriber',
            name='last_status_update',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 5, 14, 54, 16, 421601, tzinfo=utc), verbose_name='Time of last status change'),
        ),
    ]