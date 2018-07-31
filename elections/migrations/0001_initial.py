# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-07-31 18:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(db_index=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=128, unique=True)),
                ('address', models.CharField(max_length=128)),
                ('map_url', models.CharField(blank=True, max_length=255, null=True)),
                ('image_url', models.CharField(blank=True, max_length=255, null=True)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='elections.District')),
            ],
        ),
        migrations.CreateModel(
            name='Precinct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(db_index=True, unique=True)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='elections.District')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='elections.Poll')),
            ],
        ),
    ]
