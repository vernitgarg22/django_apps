# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste_notifier', '0003_subscriber_service_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='comment',
            field=models.CharField(verbose_name='Internal use only', null=True, max_length=128, blank=True),
        ),
        migrations.AddField(
            model_name='subscriber',
            name='last_status_update',
            field=models.DateTimeField(verbose_name='Time of last status change', null=True, blank=True),
        ),
    ]
