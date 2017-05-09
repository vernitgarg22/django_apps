# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParcelMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('pnum', models.CharField(max_length=25, unique=True)),
                ('relatedpnum', models.CharField(max_length=25)),
                ('propstreetcombined', models.CharField(max_length=62)),
                ('ownername1', models.CharField(max_length=35)),
                ('ownername2', models.CharField(max_length=35)),
                ('ownerstreetaddr', models.CharField(max_length=35)),
                ('ownercity', models.CharField(max_length=25)),
                ('ownerstate', models.CharField(max_length=2)),
                ('ownerzip', models.CharField(max_length=10)),
                ('xstreetname_0', models.CharField(db_column='xStreetName_0', max_length=25)),
                ('xstreetname_1', models.CharField(db_column='xStreetName_1', max_length=25)),
                ('resb_numresb', models.SmallIntegerField()),
                ('resb_occ', models.SmallIntegerField()),
                ('resb_styhgt', models.SmallIntegerField()),
                ('resb_yearbuilt', models.SmallIntegerField()),
                ('resb_bldgclass', models.SmallIntegerField()),
                ('resb_plusminus', models.SmallIntegerField()),
                ('resb_style', models.CharField(max_length=15)),
                ('resb_effage', models.SmallIntegerField()),
                ('resb_depr', models.SmallIntegerField()),
                ('resb_heat', models.SmallIntegerField()),
                ('resb_nbed', models.SmallIntegerField()),
                ('resb_fullbaths', models.SmallIntegerField()),
                ('resb_halfbaths', models.SmallIntegerField()),
                ('resb_gartype', models.SmallIntegerField(db_column='resb_garType')),
                ('resb_fireplaces', models.SmallIntegerField()),
                ('resb_exterior', models.SmallIntegerField()),
                ('resb_floorarea', models.IntegerField()),
                ('resb_groundarea', models.IntegerField()),
                ('resb_basementarea', models.IntegerField()),
                ('resb_garagearea', models.IntegerField()),
                ('resb_avestyht', models.FloatField()),
                ('resb_pricefloor', models.FloatField()),
                ('resb_priceground', models.FloatField()),
                ('resb_calcvalue', models.FloatField()),
                ('resb_value', models.FloatField()),
                ('cib_numcib', models.SmallIntegerField()),
                ('cib_occ', models.SmallIntegerField()),
                ('cib_yearbuilt', models.SmallIntegerField()),
                ('cib_bldgclass', models.SmallIntegerField()),
                ('cib_effage', models.SmallIntegerField()),
                ('cib_stories', models.SmallIntegerField()),
                ('cib_floorarea', models.FloatField()),
                ('cib_pricefloor', models.FloatField()),
                ('cib_calcvalue', models.FloatField()),
                ('cib_value', models.FloatField()),
                ('cibbedrooms', models.SmallIntegerField(db_column='CiBBedrooms')),
                ('cibunits', models.SmallIntegerField(db_column='CiBUnits')),
            ],
        ),
    ]
