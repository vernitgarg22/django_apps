# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ElectionNotification',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('notification_type', models.CharField(verbose_name='Notification type', max_length=32, default='reminder', choices=[('reminder', 'Reminder'), ('alert', 'Alert')])),
                ('day', models.DateField(verbose_name='Day on which notification should be sent')),
                ('message', models.CharField(verbose_name='Notification message', max_length=512, blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ElectionSubscriber',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('phone_number', models.CharField(verbose_name='Subscriber phone number', max_length=32, unique=True)),
                ('status', models.CharField(verbose_name='Subscriber status', max_length=32, default='inactive', choices=[('active', 'Active'), ('inactive', 'Inactive')])),
                ('created_at', models.DateTimeField(verbose_name='Time of last status change', default=timezone.now())),
                ('last_status_update', models.DateTimeField(verbose_name='Time of last status change', default=timezone.now())),
                ('latitude', models.CharField(verbose_name='Latitude', max_length=32)),
                ('longitude', models.CharField(verbose_name='Longitude', max_length=32)),
                ('address', models.CharField(verbose_name='Home address', max_length=128)),
            ],
        ),
    ]
