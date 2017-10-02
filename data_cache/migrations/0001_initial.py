# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-02 16:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=64, unique=True, verbose_name='Name')),
                ('url', models.CharField(max_length=1024, verbose_name='Data Source URL')),
            ],
        ),
        migrations.CreateModel(
            name='DataValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField()),
                ('updated', models.DateTimeField(verbose_name='Last time data was cached')),
                ('data_source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_cache.DataSource')),
            ],
        ),
    ]
