# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MessengerClient',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Name', max_length=64, unique=True)),
                ('description', models.CharField(verbose_name='Description', max_length=1024)),
                ('confirmation_message', models.CharField('Confirmation Message', max_length=2048)),
            ],
        ),

        migrations.CreateModel(
            name='MessengerPhoneNumber',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('messenger_client' , models.ForeignKey(to='messenger.MessengerClient', on_delete=models.deletion.PROTECT)),
                ('phone_number', models.CharField(verbose_name='Phone Number', max_length=10, db_index=True, unique=True)),
                ('description', models.CharField(verbose_name='Description', max_length=512, blank=True, null=True)),
            ],
        ),

        migrations.CreateModel(
            name='MessengerNotification',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('messenger_client' , models.ForeignKey(to='messenger.MessengerClient', on_delete=models.deletion.PROTECT)),
                ('day', models.DateField(verbose_name='Day on which notification should be sent')),
                ('geo_layer_url', models.CharField(verbose_name='Geo Layer URL', max_length=1024, blank=True, null=True)),
                ('formatter', models.CharField(verbose_name='Formatter class to render message', max_length=64, blank=True, null=True)),
            ],
        ),

        migrations.CreateModel(
            name='MessengerMessage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('messenger_notification' , models.ForeignKey(to='messenger.MessengerNotification', on_delete=models.deletion.PROTECT)),
                ('lang', models.CharField(verbose_name='Language', max_length=32, default='en')),
                ('message', models.CharField(verbose_name='Messae', max_length=2048, blank=True, null=True)),
            ],
        ),

        migrations.CreateModel(
            name='MessengerSubscriber',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('messenger_client' , models.ForeignKey(to='messenger.MessengerClient', on_delete=models.deletion.PROTECT)),
                ('phone_number', models.CharField(verbose_name='Subscriber phone number', max_length=32, unique=True)),
                ('status', models.CharField(verbose_name='Subscriber status', max_length=32, default='inactive', choices=[('active', 'Active'), ('inactive', 'Inactive')])),
                ('address', models.CharField(verbose_name='Home address', max_length=128)),
                ('latitude', models.CharField(verbose_name='Latitude', max_length=32)),
                ('longitude', models.CharField(verbose_name='Longitude', max_length=32)),
                ('lang', models.CharField(verbose_name='Preferred Language', max_length=32, blank=True, null=True)),
                ('created_at', models.DateTimeField(verbose_name='Time of last status change', default=timezone.now())),
                ('last_status_update', models.DateTimeField(verbose_name='Time of last status change', default=timezone.now())),
            ],
        ),
    ]
