# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste_notifier', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='phone_number',
            field=models.CharField(unique=True, max_length=32, verbose_name='Subscriber phone number'),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], max_length=32, verbose_name='Subscriber status (for soft deletes)', default='inactive'),
        ),
    ]
