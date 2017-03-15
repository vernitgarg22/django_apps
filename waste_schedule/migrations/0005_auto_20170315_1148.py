# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste_schedule', '0004_auto_20170314_1502'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wastearea',
            options={'ordering': ['order_val']},
        ),
        migrations.AddField(
            model_name='wastearea',
            name='order_val',
            field=models.IntegerField(verbose_name='Waste area ordering value', null=True),
        ),
    ]
