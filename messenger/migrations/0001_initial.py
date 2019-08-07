# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils import timezone


# class Notification(models.Model):

#     app_label = 'messenger'

#     day = models.DateField('Day on which notification should be sent')
#     message = models.CharField('Message', max_length=1024, blank=True, null=True)
#     geo_layer_url = models.CharField('Geo Layer URL', max_length=1024, blank=True, null=True)
#     messenger_type = models.ForeignKey(MessengerType)


# class Subscriber(models.Model):

#     app_label = 'messenger'

#     STATUS_CHOICES = (
#         ('active', 'Active'),
#         ('inactive', 'Inactive'),
#     )

#     phone_number = models.CharField('Subscriber phone number', unique=True, max_length=32)
#     status = models.CharField('Subscriber status', max_length=32, choices=STATUS_CHOICES, default='inactive')
#     address = models.CharField('Home address', max_length=128)
#     latitude = models.CharField('Latitude', max_length=32)
#     longitude = models.CharField('Longitude', max_length=32)
#     created_at = models.DateTimeField('Time of initial subscription', default=timezone.now())
#     last_status_update = models.DateTimeField('Time of last status change', default=timezone.now())



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
            ],
        ),
        migrations.CreateModel(
            name='MessengerNotification',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('messenger_client' , models.ForeignKey(to='messenger.MessengerClient', on_delete=models.deletion.PROTECT)),
                ('day', models.DateField(verbose_name='Day on which notification should be sent')),
                ('message', models.CharField(verbose_name='Messae', max_length=2048, blank=True, null=True)),
                ('geo_layer_url', models.CharField(verbose_name='Geo Layer URL', max_length=1024, blank=True, null=True)),
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
                ('created_at', models.DateTimeField(verbose_name='Time of last status change', default=timezone.now())),
                ('last_status_update', models.DateTimeField(verbose_name='Time of last status change', default=timezone.now())),
            ],
        ),
    ]
