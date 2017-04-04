# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import re
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('phone_number', models.CharField(verbose_name='Subscriber phone number', max_length=32)),
                ('waste_area_ids', models.CharField(verbose_name='Subscriber Waste area(s)', validators=[django.core.validators.RegexValidator(re.compile('^[\\d,]+\\Z', 32), 'Enter only digits separated by commas.', 'invalid')], max_length=64)),
                ('status', models.CharField(verbose_name='Subscriber status (for soft deletes)', choices=[('active', 'Active'), ('deleted', 'Deleted')], default='deleted', max_length=32)),
            ],
        ),
    ]
