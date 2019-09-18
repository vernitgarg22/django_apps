# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-09-10 18:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0006_20190906_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='messengerphonenumber',
            name='number_type',
            field=models.CharField(choices=[('sender', 'Notificaton Sender'), ('text_signup', 'Text Signup')], default='sender', max_length=32, verbose_name='Number Type'),
        )
    ]