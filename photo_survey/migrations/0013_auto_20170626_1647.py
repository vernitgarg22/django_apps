# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_survey', '0012_auto_20170626_1644'),
    ]

    operations = [
        migrations.RenameField(
            model_name='surveytemplate',
            old_name='answer_trigger_result',
            new_name='answer_trigger_action',
        ),
    ]
