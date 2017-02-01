# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WasteItem',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('description', models.CharField(verbose_name='Waste item description', max_length=200)),
                ('destination', models.CharField(verbose_name='Appropriate waste destination', max_length=32)),
                ('notes', models.CharField(verbose_name='Special details to note', max_length=300)),
                ('keywords', models.CharField(default='', verbose_name='Keywords associated with the item', max_length=300)),
            ],
        ),
    ]
