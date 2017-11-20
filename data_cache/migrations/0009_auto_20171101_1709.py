# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-01 21:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_cache', '0008_auto_20171026_1318'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=64, unique=True, verbose_name='Name')),
            ],
        ),
        migrations.AddField(
            model_name='datasource',
            name='data_set',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data_cache.DataSet'),
        ),
    ]