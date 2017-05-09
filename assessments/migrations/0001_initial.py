# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('pnum', models.CharField(max_length=25)),
                ('saledate', models.DateTimeField(blank=True, null=True)),
                ('addresscombined', models.CharField(max_length=62)),
                ('saleprice', models.DecimalField(max_digits=18, decimal_places=0)),
                ('terms', models.CharField(max_length=20)),
                ('instr', models.CharField(max_length=3)),
                ('grantor', models.CharField(max_length=35)),
                ('grantee', models.CharField(max_length=35)),
            ],
        ),
    ]
