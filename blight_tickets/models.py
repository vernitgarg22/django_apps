from django.db import models


class Tblztickets(models.Model):
    zticketid = models.IntegerField(db_column='ZTicketID')  # Field name made lowercase.
    ticketnumber = models.CharField(db_column='TicketNumber', primary_key=True, max_length=12)  # Field name made lowercase.
    agencyid = models.IntegerField(db_column='AgencyID')  # Field name made lowercase.
    violstreetnumber = models.IntegerField(db_column='ViolStreetNumber')  # Field name made lowercase.
    violstreetname = models.IntegerField(db_column='ViolStreetName')  # Field name made lowercase.
    violzipcode = models.CharField(db_column='ViolZipCode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    violdescid = models.IntegerField(db_column='ViolDescID')  # Field name made lowercase.
    issuedate = models.DateTimeField(db_column='IssueDate')  # Field name made lowercase.
    issuetime = models.DateTimeField(db_column='IssueTime')  # Field name made lowercase.
    courttime = models.IntegerField(db_column='CourtTime', blank=True, null=True)  # Field name made lowercase.
    initialcourttime = models.IntegerField(db_column='InitialCourtTime', blank=True, null=True)  # Field name made lowercase.
    courtdate = models.DateTimeField(db_column='CourtDate', blank=True, null=True)  # Field name made lowercase.
    canceledby = models.IntegerField(db_column='CanceledBy', blank=True, null=True)  # Field name made lowercase.
    canceldate = models.DateTimeField(db_column='CancelDate', blank=True, null=True)  # Field name made lowercase.
    cancelreason = models.CharField(db_column='CancelReason', max_length=50, blank=True, null=True)  # Field name made lowercase.
    voidticket = models.IntegerField(db_column='VoidTicket', blank=True, null=True)  # Field name made lowercase.
    origfineamt = models.IntegerField(db_column='OrigFineAmt')  # Field name made lowercase.
    newfineamt = models.DecimalField(db_column='NewFineAmt', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    adjjudgmentamt = models.DecimalField(db_column='AdjJudgmentAmt', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    jsa = models.DecimalField(db_column='JSA', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    adminfee = models.DecimalField(db_column='AdminFee', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    latefee = models.DecimalField(db_column='LateFee', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    discamt = models.DecimalField(db_column='DiscAmt', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    remediationcost = models.DecimalField(db_column='RemediationCost', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    serve = models.IntegerField(db_column='Serve', blank=True, null=True)  # Field name made lowercase.
    cityoffsign = models.IntegerField(db_column='CityOffSign')  # Field name made lowercase.
    courtcnsl = models.IntegerField(db_column='CourtCnsl', blank=True, null=True)  # Field name made lowercase.
    courtcnsldt = models.CharField(db_column='CourtCnslDt', max_length=10, blank=True, null=True)  # Field name made lowercase.
    zticketuserid = models.IntegerField(db_column='ZTicketUserID')  # Field name made lowercase.
    zticketupdatedt = models.DateTimeField(db_column='ZTicketUpdateDt')  # Field name made lowercase.
    chptrid = models.IntegerField(db_column='ChptrID')  # Field name made lowercase.
    repeatoffenderflag = models.IntegerField(db_column='RepeatOffenderFlag', blank=True, null=True)  # Field name made lowercase.
    inspectornote = models.TextField(db_column='InspectorNote', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    attorneyid = models.IntegerField(db_column='AttorneyID', blank=True, null=True)  # Field name made lowercase.
    tickettype = models.CharField(db_column='TicketType', max_length=10)  # Field name made lowercase.
    crtrmid = models.IntegerField(db_column='CrtRmID')  # Field name made lowercase.
    clearused = models.IntegerField(db_column='ClearUsed', blank=True, null=True)  # Field name made lowercase.
    clearnum = models.CharField(db_column='ClearNum', max_length=50, blank=True, null=True)  # Field name made lowercase.
    clearrecordid = models.IntegerField(db_column='ClearRecordID', blank=True, null=True)  # Field name made lowercase.
    modifiedby = models.IntegerField(db_column='ModifiedBy', blank=True, null=True)  # Field name made lowercase.
    modifieddt = models.DateTimeField(db_column='ModifiedDT', blank=True, null=True)  # Field name made lowercase.
    stay = models.IntegerField(db_column='Stay', blank=True, null=True)  # Field name made lowercase.
    ticketprintflag = models.IntegerField(db_column='TicketPrintFlag', blank=True, null=True)  # Field name made lowercase.
    ticketprintdt = models.DateTimeField(db_column='TicketPrintDT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblZTickets'
