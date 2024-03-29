# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-18 19:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tblztickets',
            fields=[
                ('zticketid', models.IntegerField(db_column='ZTicketID')),
                ('ticketnumber', models.CharField(db_column='TicketNumber', max_length=12, primary_key=True, serialize=False)),
                ('agencyid', models.IntegerField(db_column='AgencyID')),
                ('violstreetnumber', models.IntegerField(db_column='ViolStreetNumber')),
                ('violstreetname', models.IntegerField(db_column='ViolStreetName')),
                ('violzipcode', models.CharField(blank=True, db_column='ViolZipCode', max_length=20, null=True)),
                ('violdescid', models.IntegerField(db_column='ViolDescID')),
                ('issuedate', models.DateTimeField(db_column='IssueDate')),
                ('issuetime', models.DateTimeField(db_column='IssueTime')),
                ('courttime', models.IntegerField(blank=True, db_column='CourtTime', null=True)),
                ('initialcourttime', models.IntegerField(blank=True, db_column='InitialCourtTime', null=True)),
                ('courtdate', models.DateTimeField(blank=True, db_column='CourtDate', null=True)),
                ('canceledby', models.IntegerField(blank=True, db_column='CanceledBy', null=True)),
                ('canceldate', models.DateTimeField(blank=True, db_column='CancelDate', null=True)),
                ('cancelreason', models.CharField(blank=True, db_column='CancelReason', max_length=50, null=True)),
                ('voidticket', models.IntegerField(blank=True, db_column='VoidTicket', null=True)),
                ('origfineamt', models.IntegerField(db_column='OrigFineAmt')),
                ('newfineamt', models.DecimalField(blank=True, db_column='NewFineAmt', decimal_places=2, max_digits=18, null=True)),
                ('adjjudgmentamt', models.DecimalField(blank=True, db_column='AdjJudgmentAmt', decimal_places=2, max_digits=18, null=True)),
                ('jsa', models.DecimalField(blank=True, db_column='JSA', decimal_places=0, max_digits=18, null=True)),
                ('adminfee', models.DecimalField(blank=True, db_column='AdminFee', decimal_places=0, max_digits=18, null=True)),
                ('latefee', models.DecimalField(blank=True, db_column='LateFee', decimal_places=2, max_digits=18, null=True)),
                ('discamt', models.DecimalField(blank=True, db_column='DiscAmt', decimal_places=2, max_digits=18, null=True)),
                ('remediationcost', models.DecimalField(blank=True, db_column='RemediationCost', decimal_places=2, max_digits=18, null=True)),
                ('serve', models.IntegerField(blank=True, db_column='Serve', null=True)),
                ('cityoffsign', models.IntegerField(db_column='CityOffSign')),
                ('courtcnsl', models.IntegerField(blank=True, db_column='CourtCnsl', null=True)),
                ('courtcnsldt', models.CharField(blank=True, db_column='CourtCnslDt', max_length=10, null=True)),
                ('zticketuserid', models.IntegerField(db_column='ZTicketUserID')),
                ('zticketupdatedt', models.DateTimeField(db_column='ZTicketUpdateDt')),
                ('chptrid', models.IntegerField(db_column='ChptrID')),
                ('repeatoffenderflag', models.IntegerField(blank=True, db_column='RepeatOffenderFlag', null=True)),
                ('inspectornote', models.TextField(blank=True, db_column='InspectorNote', null=True)),
                ('attorneyid', models.IntegerField(blank=True, db_column='AttorneyID', null=True)),
                ('tickettype', models.CharField(db_column='TicketType', max_length=10)),
                ('crtrmid', models.IntegerField(db_column='CrtRmID')),
                ('clearused', models.IntegerField(blank=True, db_column='ClearUsed', null=True)),
                ('clearnum', models.CharField(blank=True, db_column='ClearNum', max_length=50, null=True)),
                ('clearrecordid', models.IntegerField(blank=True, db_column='ClearRecordID', null=True)),
                ('modifiedby', models.IntegerField(blank=True, db_column='ModifiedBy', null=True)),
                ('modifieddt', models.DateTimeField(blank=True, db_column='ModifiedDT', null=True)),
                ('stay', models.IntegerField(blank=True, db_column='Stay', null=True)),
                ('ticketprintflag', models.IntegerField(blank=True, db_column='TicketPrintFlag', null=True)),
                ('ticketprintdt', models.DateTimeField(blank=True, db_column='TicketPrintDT', null=True)),
            ],
            options={
                'db_table': 'tblZTickets',
                # 'managed': False,
            },
        ),
    ]
