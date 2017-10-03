from django.db import models


class Affiliates(models.Model):
    affiliateid = models.AutoField(db_column='AffiliateId', primary_key=True)  # Field name made lowercase.
    vendorid = models.ForeignKey('Vendors', models.DO_NOTHING, db_column='VendorId', blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    cpc = models.FloatField(db_column='CPC')  # Field name made lowercase.
    clicks = models.IntegerField(db_column='Clicks')  # Field name made lowercase.
    cpa = models.FloatField(db_column='CPA')  # Field name made lowercase.
    acquisitions = models.IntegerField(db_column='Acquisitions')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Affiliates'


class AnalyticsEventdata(models.Model):
    eventdataid = models.BigAutoField(db_column='EventDataId', primary_key=True)  # Field name made lowercase.
    pageviewid = models.BigIntegerField(db_column='PageViewId')  # Field name made lowercase.
    visitorid = models.CharField(db_column='VisitorId', max_length=36)  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    tabid = models.IntegerField(db_column='TabId')  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserId')  # Field name made lowercase.
    portalaliasid = models.IntegerField(db_column='PortalAliasId')  # Field name made lowercase.
    eventcategory = models.CharField(db_column='EventCategory', max_length=256)  # Field name made lowercase.
    eventname = models.CharField(db_column='EventName', max_length=256)  # Field name made lowercase.
    eventaction = models.CharField(db_column='EventAction', max_length=256)  # Field name made lowercase.
    eventvalue = models.CharField(db_column='EventValue', max_length=2000)  # Field name made lowercase.
    eventdate = models.DateTimeField(db_column='EventDate')  # Field name made lowercase.
    contentitemid = models.IntegerField(db_column='ContentItemId')  # Field name made lowercase.
    dateid = models.IntegerField(db_column='DateId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Analytics_EventData'


class AnalyticsFactConversions(models.Model):
    factid = models.AutoField(db_column='FactId', primary_key=True)  # Field name made lowercase.
    dateid = models.IntegerField(db_column='DateId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    pageid = models.IntegerField(db_column='PageId')  # Field name made lowercase.
    eventname = models.CharField(db_column='EventName', max_length=200)  # Field name made lowercase.
    eventvalue = models.CharField(db_column='EventValue', max_length=200)  # Field name made lowercase.
    eventcount = models.IntegerField(db_column='EventCount')  # Field name made lowercase.
    contentitemid = models.IntegerField(db_column='ContentItemId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Analytics_Fact_Conversions'


class AnalyticsFactDevices(models.Model):
    factid = models.AutoField(db_column='FactId', primary_key=True)  # Field name made lowercase.
    dateid = models.IntegerField(db_column='DateId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    pageid = models.IntegerField(db_column='PageId')  # Field name made lowercase.
    device = models.IntegerField(db_column='Device')  # Field name made lowercase.
    operatingsystem = models.CharField(db_column='OperatingSystem', max_length=200)  # Field name made lowercase.
    pageviews = models.IntegerField(db_column='PageViews')  # Field name made lowercase.
    contentitemid = models.IntegerField(db_column='ContentItemId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Analytics_Fact_Devices'


class AnalyticsFactExitpages(models.Model):
    factid = models.AutoField(db_column='FactId', primary_key=True)  # Field name made lowercase.
    dateid = models.IntegerField(db_column='DateId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    pageid = models.IntegerField(db_column='PageId')  # Field name made lowercase.
    exitpage = models.CharField(db_column='ExitPage', max_length=200)  # Field name made lowercase.
    pageviews = models.IntegerField(db_column='PageViews')  # Field name made lowercase.
    contentitemid = models.IntegerField(db_column='ContentItemId')  # Field name made lowercase.
    exitpageid = models.IntegerField(db_column='ExitPageId')  # Field name made lowercase.
    exitpagecontentitemid = models.IntegerField(db_column='ExitPageContentItemId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Analytics_Fact_ExitPages'


class AnalyticsFactLinkclicked(models.Model):
    factid = models.AutoField(db_column='FactId', primary_key=True)  # Field name made lowercase.
    dateid = models.IntegerField(db_column='DateId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    pageid = models.IntegerField(db_column='PageId')  # Field name made lowercase.
    link = models.CharField(db_column='Link', max_length=2000)  # Field name made lowercase.
    linkcount = models.IntegerField(db_column='LinkCount')  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserId')  # Field name made lowercase.
    visitorid = models.CharField(db_column='VisitorId', max_length=36)  # Field name made lowercase.
    contentitemid = models.IntegerField(db_column='ContentItemId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Analytics_Fact_LinkClicked'


class AnalyticsFactPageviews(models.Model):
    factid = models.AutoField(db_column='FactId', primary_key=True)  # Field name made lowercase.
    dateid = models.IntegerField(db_column='DateId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    pageid = models.IntegerField(db_column='PageId')  # Field name made lowercase.
    pagename = models.CharField(db_column='PageName', max_length=200)  # Field name made lowercase.
    pageviews = models.IntegerField(db_column='PageViews')  # Field name made lowercase.
    timeonpage = models.IntegerField(db_column='TimeOnPage')  # Field name made lowercase.
    contentitemid = models.IntegerField(db_column='ContentItemId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Analytics_Fact_PageViews'


class AnalyticsFactReferrers(models.Model):
    factid = models.AutoField(db_column='FactId', primary_key=True)  # Field name made lowercase.
    dateid = models.IntegerField(db_column='DateId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    pageid = models.IntegerField(db_column='PageId')  # Field name made lowercase.
    channel = models.IntegerField(db_column='Channel')  # Field name made lowercase.
    referrerhost = models.CharField(db_column='ReferrerHost', max_length=200)  # Field name made lowercase.
    referrerdetail = models.CharField(db_column='ReferrerDetail', max_length=200)  # Field name made lowercase.
    referrerpageid = models.IntegerField(db_column='ReferrerPageId')  # Field name made lowercase.
    pageviews = models.IntegerField(db_column='PageViews')  # Field name made lowercase.
    contentitemid = models.IntegerField(db_column='ContentItemId')  # Field name made lowercase.
    contentitemreferrerid = models.IntegerField(db_column='ContentItemReferrerId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Analytics_Fact_Referrers'


class AnalyticsFactSessions(models.Model):
    factid = models.AutoField(db_column='FactId', primary_key=True)  # Field name made lowercase.
    dateid = models.IntegerField(db_column='DateId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    sessionguid = models.CharField(db_column='SessionGuid', max_length=36)  # Field name made lowercase.
    pageid = models.IntegerField(db_column='PageId')  # Field name made lowercase.
    pageviews = models.IntegerField(db_column='PageViews')  # Field name made lowercase.
    timeonpage = models.IntegerField(db_column='TimeOnPage')  # Field name made lowercase.
    contentitemid = models.IntegerField(db_column='ContentItemId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Analytics_Fact_Sessions'


class AnalyticsFactUsers(models.Model):
    factid = models.AutoField(db_column='FactId', primary_key=True)  # Field name made lowercase.
    dateid = models.IntegerField(db_column='DateId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserId')  # Field name made lowercase.
    pageid = models.IntegerField(db_column='PageId')  # Field name made lowercase.
    pageviews = models.IntegerField(db_column='PageViews')  # Field name made lowercase.
    timeonpage = models.IntegerField(db_column='TimeOnPage')  # Field name made lowercase.
    contentitemid = models.IntegerField(db_column='ContentItemId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Analytics_Fact_Users'


class AnalyticsFactVisitors(models.Model):
    factid = models.AutoField(db_column='FactId', primary_key=True)  # Field name made lowercase.
    dateid = models.IntegerField(db_column='DateId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    visitorguid = models.CharField(db_column='VisitorGuid', max_length=36)  # Field name made lowercase.
    pageid = models.IntegerField(db_column='PageId')  # Field name made lowercase.
    pageviews = models.IntegerField(db_column='PageViews')  # Field name made lowercase.
    timeonpage = models.IntegerField(db_column='TimeOnPage')  # Field name made lowercase.
    contentitemid = models.IntegerField(db_column='ContentItemId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Analytics_Fact_Visitors'


class AnalyticsPageviews(models.Model):
    pageviewid = models.BigAutoField(db_column='PageViewId', primary_key=True)  # Field name made lowercase.
    dateid = models.IntegerField(db_column='DateId')  # Field name made lowercase.
    visitorguid = models.CharField(db_column='VisitorGuid', max_length=36)  # Field name made lowercase.
    sessionguid = models.CharField(db_column='SessionGuid', max_length=36)  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    tabid = models.IntegerField(db_column='TabId')  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserId')  # Field name made lowercase.
    device = models.IntegerField(db_column='Device')  # Field name made lowercase.
    operatingsystem = models.CharField(db_column='OperatingSystem', max_length=200)  # Field name made lowercase.
    channel = models.IntegerField(db_column='Channel')  # Field name made lowercase.
    referrerhost = models.CharField(db_column='ReferrerHost', max_length=200)  # Field name made lowercase.
    referrerdetail = models.CharField(db_column='ReferrerDetail', max_length=200)  # Field name made lowercase.
    referrerpageid = models.IntegerField(db_column='ReferrerPageId')  # Field name made lowercase.
    exitpage = models.CharField(db_column='ExitPage', max_length=200)  # Field name made lowercase.
    totalseconds = models.IntegerField(db_column='TotalSeconds')  # Field name made lowercase.
    useragent = models.CharField(db_column='UserAgent', max_length=200)  # Field name made lowercase.
    pagelanguage = models.CharField(db_column='PageLanguage', max_length=10)  # Field name made lowercase.
    ipaddress = models.CharField(db_column='IPAddress', max_length=50)  # Field name made lowercase.
    urlquery = models.CharField(db_column='UrlQuery', max_length=200)  # Field name made lowercase.
    contentitemid = models.IntegerField(db_column='ContentItemId')  # Field name made lowercase.
    contentitemreferrerid = models.IntegerField(db_column='ContentItemReferrerId')  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Analytics_PageViews'


class Announcements(models.Model):
    itemid = models.AutoField(db_column='ItemID', primary_key=True)  # Field name made lowercase.
    moduleid = models.ForeignKey('Modules', models.DO_NOTHING, db_column='ModuleID')  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=150, blank=True, null=True)  # Field name made lowercase.
    url = models.CharField(db_column='URL', max_length=250, blank=True, null=True)  # Field name made lowercase.
    expiredate = models.DateTimeField(db_column='ExpireDate', blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    vieworder = models.IntegerField(db_column='ViewOrder', blank=True, null=True)  # Field name made lowercase.
    createdbyuser = models.IntegerField(db_column='CreatedByUser')  # Field name made lowercase.
    publishdate = models.DateTimeField(db_column='PublishDate', blank=True, null=True)  # Field name made lowercase.
    imagesource = models.CharField(db_column='ImageSource', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Announcements'


class Anonymoususers(models.Model):
    userid = models.CharField(db_column='UserID', primary_key=True, max_length=36)  # Field name made lowercase.
    portalid = models.ForeignKey('Portals', models.DO_NOTHING, db_column='PortalID')  # Field name made lowercase.
    tabid = models.IntegerField(db_column='TabID')  # Field name made lowercase.
    creationdate = models.DateTimeField(db_column='CreationDate')  # Field name made lowercase.
    lastactivedate = models.DateTimeField(db_column='LastActiveDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AnonymousUsers'
        unique_together = (('userid', 'portalid'),)


class Assemblies(models.Model):
    assemblyid = models.AutoField(db_column='AssemblyID', primary_key=True)  # Field name made lowercase.
    packageid = models.ForeignKey('Packages', models.DO_NOTHING, db_column='PackageID', blank=True, null=True)  # Field name made lowercase.
    assemblyname = models.CharField(db_column='AssemblyName', max_length=250)  # Field name made lowercase.
    version = models.CharField(db_column='Version', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Assemblies'


class Authentication(models.Model):
    authenticationid = models.AutoField(db_column='AuthenticationID', primary_key=True)  # Field name made lowercase.
    packageid = models.ForeignKey('Packages', models.DO_NOTHING, db_column='PackageID')  # Field name made lowercase.
    authenticationtype = models.CharField(db_column='AuthenticationType', max_length=100)  # Field name made lowercase.
    isenabled = models.BooleanField(db_column='IsEnabled')  # Field name made lowercase.
    settingscontrolsrc = models.CharField(db_column='SettingsControlSrc', max_length=250)  # Field name made lowercase.
    logincontrolsrc = models.CharField(db_column='LoginControlSrc', max_length=250)  # Field name made lowercase.
    logoffcontrolsrc = models.CharField(db_column='LogoffControlSrc', max_length=250)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Authentication'


class Banners(models.Model):
    bannerid = models.AutoField(db_column='BannerId', primary_key=True)  # Field name made lowercase.
    vendorid = models.ForeignKey('Vendors', models.DO_NOTHING, db_column='VendorId')  # Field name made lowercase.
    imagefile = models.CharField(db_column='ImageFile', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bannername = models.CharField(db_column='BannerName', max_length=100)  # Field name made lowercase.
    impressions = models.IntegerField(db_column='Impressions')  # Field name made lowercase.
    cpm = models.FloatField(db_column='CPM')  # Field name made lowercase.
    views = models.IntegerField(db_column='Views')  # Field name made lowercase.
    clickthroughs = models.IntegerField(db_column='ClickThroughs')  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    createdbyuser = models.CharField(db_column='CreatedByUser', max_length=100)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate')  # Field name made lowercase.
    bannertypeid = models.IntegerField(db_column='BannerTypeId', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    groupname = models.CharField(db_column='GroupName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    criteria = models.BooleanField(db_column='Criteria')  # Field name made lowercase.
    url = models.CharField(db_column='URL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    width = models.IntegerField(db_column='Width')  # Field name made lowercase.
    height = models.IntegerField(db_column='Height')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Banners'


class CkeSettings(models.Model):
    settingname = models.CharField(db_column='SettingName', primary_key=True, max_length=300)  # Field name made lowercase.
    settingvalue = models.TextField(db_column='SettingValue')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CKE_Settings'


class Classification(models.Model):
    classificationid = models.AutoField(db_column='ClassificationId', primary_key=True)  # Field name made lowercase.
    classificationname = models.CharField(db_column='ClassificationName', max_length=200)  # Field name made lowercase.
    parentid = models.ForeignKey('self', models.DO_NOTHING, db_column='ParentId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Classification'


class ContentitemSlug(models.Model):
    tabid = models.OneToOneField('Tabs', models.DO_NOTHING, db_column='TabId', primary_key=True)  # Field name made lowercase.
    contentitemid = models.ForeignKey('Contentitems', models.DO_NOTHING, db_column='ContentItemId', blank=True, null=True)  # Field name made lowercase.
    httpstatus = models.IntegerField(db_column='HttpStatus')  # Field name made lowercase.
    slug = models.CharField(db_column='Slug', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ContentItem_Slug'
        unique_together = (('tabid', 'slug'),)


class Contentitems(models.Model):
    contentitemid = models.AutoField(db_column='ContentItemID', primary_key=True)  # Field name made lowercase.
    content = models.TextField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    contenttypeid = models.ForeignKey('Contenttypes', models.DO_NOTHING, db_column='ContentTypeID')  # Field name made lowercase.
    tabid = models.IntegerField(db_column='TabID')  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleID')  # Field name made lowercase.
    contentkey = models.CharField(db_column='ContentKey', max_length=250, blank=True, null=True)  # Field name made lowercase.
    indexed = models.BooleanField(db_column='Indexed')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.
    stateid = models.ForeignKey('Contentworkflowstates', models.DO_NOTHING, db_column='StateID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ContentItems'


class ContentitemsMetadata(models.Model):
    contentitemmetadataid = models.AutoField(db_column='ContentItemMetaDataID', primary_key=True)  # Field name made lowercase.
    contentitemid = models.ForeignKey(Contentitems, models.DO_NOTHING, db_column='ContentItemID')  # Field name made lowercase.
    metadataid = models.ForeignKey('Metadata', models.DO_NOTHING, db_column='MetaDataID')  # Field name made lowercase.
    metadatavalue = models.TextField(db_column='MetaDataValue', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ContentItems_MetaData'


class ContentitemsTags(models.Model):
    contentitemtagid = models.AutoField(db_column='ContentItemTagID', primary_key=True)  # Field name made lowercase.
    contentitemid = models.ForeignKey(Contentitems, models.DO_NOTHING, db_column='ContentItemID')  # Field name made lowercase.
    termid = models.ForeignKey('TaxonomyTerms', models.DO_NOTHING, db_column='TermID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ContentItems_Tags'
        unique_together = (('contentitemid', 'termid'),)


class ContentlayoutVersions(models.Model):
    moduleid = models.OneToOneField('Modules', models.DO_NOTHING, db_column='ModuleId', primary_key=True)  # Field name made lowercase.
    version = models.IntegerField(db_column='Version')  # Field name made lowercase.
    columnsizes = models.CharField(db_column='ColumnSizes', max_length=50)  # Field name made lowercase.
    columncssclasses = models.CharField(db_column='ColumnCssClasses', max_length=256)  # Field name made lowercase.
    arecustomcolumnsizes = models.BooleanField(db_column='AreCustomColumnSizes')  # Field name made lowercase.
    ispublished = models.BooleanField(db_column='IsPublished')  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate')  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ContentLayout_Versions'
        unique_together = (('moduleid', 'version'),)


class ContentpersonalizationPersonalizedtabs(models.Model):
    tabid = models.OneToOneField('Tabs', models.DO_NOTHING, db_column='TabId', primary_key=True)  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    originaltabid = models.IntegerField(db_column='OriginalTabId')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=256)  # Field name made lowercase.
    priority = models.IntegerField(db_column='Priority')  # Field name made lowercase.
    rules = models.TextField(db_column='Rules')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ContentPersonalization_PersonalizedTabs'
        unique_together = (('originaltabid', 'name'),)


class Contenttypes(models.Model):
    contenttypeid = models.AutoField(db_column='ContentTypeID', primary_key=True)  # Field name made lowercase.
    contenttype = models.CharField(db_column='ContentType', unique=True, max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ContentTypes'


class Contentworkflowactions(models.Model):
    actionid = models.AutoField(db_column='ActionId', primary_key=True)  # Field name made lowercase.
    contenttypeid = models.ForeignKey(Contenttypes, models.DO_NOTHING, db_column='ContentTypeId')  # Field name made lowercase.
    actiontype = models.CharField(db_column='ActionType', max_length=50)  # Field name made lowercase.
    actionsource = models.CharField(db_column='ActionSource', max_length=256)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ContentWorkflowActions'
        unique_together = (('contenttypeid', 'actiontype'),)


class Contentworkflowlogs(models.Model):
    workflowlogid = models.AutoField(db_column='WorkflowLogID', primary_key=True)  # Field name made lowercase.
    action = models.CharField(db_column='Action', max_length=40)  # Field name made lowercase.
    comment = models.TextField(db_column='Comment')  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date')  # Field name made lowercase.
    user = models.IntegerField(db_column='User')  # Field name made lowercase.
    workflowid = models.ForeignKey('Contentworkflows', models.DO_NOTHING, db_column='WorkflowID')  # Field name made lowercase.
    contentitemid = models.ForeignKey(Contentitems, models.DO_NOTHING, db_column='ContentItemID')  # Field name made lowercase.
    type = models.IntegerField(db_column='Type')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ContentWorkflowLogs'


class Contentworkflowsources(models.Model):
    sourceid = models.AutoField(db_column='SourceID', primary_key=True)  # Field name made lowercase.
    workflowid = models.ForeignKey('Contentworkflows', models.DO_NOTHING, db_column='WorkflowID')  # Field name made lowercase.
    sourcename = models.CharField(db_column='SourceName', max_length=20)  # Field name made lowercase.
    sourcetype = models.CharField(db_column='SourceType', max_length=250)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ContentWorkflowSources'
        unique_together = (('workflowid', 'sourcename'),)


class Contentworkflowstatepermission(models.Model):
    workflowstatepermissionid = models.AutoField(db_column='WorkflowStatePermissionID', primary_key=True)  # Field name made lowercase.
    stateid = models.ForeignKey('Contentworkflowstates', models.DO_NOTHING, db_column='StateID')  # Field name made lowercase.
    permissionid = models.ForeignKey('Permission', models.DO_NOTHING, db_column='PermissionID')  # Field name made lowercase.
    allowaccess = models.BooleanField(db_column='AllowAccess')  # Field name made lowercase.
    roleid = models.IntegerField(db_column='RoleID', blank=True, null=True)  # Field name made lowercase.
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='UserID', blank=True, null=True)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ContentWorkflowStatePermission'
        unique_together = (('stateid', 'permissionid', 'roleid', 'userid'),)


class Contentworkflowstates(models.Model):
    stateid = models.AutoField(db_column='StateID', primary_key=True)  # Field name made lowercase.
    workflowid = models.ForeignKey('Contentworkflows', models.DO_NOTHING, db_column='WorkflowID')  # Field name made lowercase.
    statename = models.CharField(db_column='StateName', max_length=40)  # Field name made lowercase.
    order = models.IntegerField(db_column='Order')  # Field name made lowercase.
    isactive = models.BooleanField(db_column='IsActive')  # Field name made lowercase.
    sendemail = models.BooleanField(db_column='SendEmail')  # Field name made lowercase.
    sendmessage = models.BooleanField(db_column='SendMessage')  # Field name made lowercase.
    isdisposalstate = models.BooleanField(db_column='IsDisposalState')  # Field name made lowercase.
    oncompletemessagesubject = models.CharField(db_column='OnCompleteMessageSubject', max_length=256)  # Field name made lowercase.
    oncompletemessagebody = models.CharField(db_column='OnCompleteMessageBody', max_length=1024)  # Field name made lowercase.
    ondiscardmessagesubject = models.CharField(db_column='OnDiscardMessageSubject', max_length=256)  # Field name made lowercase.
    ondiscardmessagebody = models.CharField(db_column='OnDiscardMessageBody', max_length=1024)  # Field name made lowercase.
    issystem = models.BooleanField(db_column='IsSystem')  # Field name made lowercase.
    sendnotification = models.BooleanField(db_column='SendNotification')  # Field name made lowercase.
    sendnotificationtoadministrators = models.BooleanField(db_column='SendNotificationToAdministrators')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ContentWorkflowStates'
        unique_together = (('workflowid', 'statename'),)


class Contentworkflows(models.Model):
    workflowid = models.AutoField(db_column='WorkflowID', primary_key=True)  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalID', blank=True, null=True)  # Field name made lowercase.
    workflowname = models.CharField(db_column='WorkflowName', max_length=40)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=256, blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.BooleanField(db_column='IsDeleted')  # Field name made lowercase.
    startaftercreating = models.BooleanField(db_column='StartAfterCreating')  # Field name made lowercase.
    startafterediting = models.BooleanField(db_column='StartAfterEditing')  # Field name made lowercase.
    dispositionenabled = models.BooleanField(db_column='DispositionEnabled')  # Field name made lowercase.
    issystem = models.BooleanField(db_column='IsSystem')  # Field name made lowercase.
    workflowkey = models.CharField(db_column='WorkflowKey', max_length=40)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ContentWorkflows'
        unique_together = (('portalid', 'workflowname'),)


class CoremessagingMessageattachments(models.Model):
    messageattachmentid = models.AutoField(db_column='MessageAttachmentID', primary_key=True)  # Field name made lowercase.
    messageid = models.ForeignKey('CoremessagingMessages', models.DO_NOTHING, db_column='MessageID')  # Field name made lowercase.
    fileid = models.IntegerField(db_column='FileID', blank=True, null=True)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CoreMessaging_MessageAttachments'


class CoremessagingMessagerecipients(models.Model):
    recipientid = models.AutoField(db_column='RecipientID', primary_key=True)  # Field name made lowercase.
    messageid = models.ForeignKey('CoremessagingMessages', models.DO_NOTHING, db_column='MessageID')  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserID')  # Field name made lowercase.
    read = models.BooleanField(db_column='Read')  # Field name made lowercase.
    archived = models.BooleanField(db_column='Archived')  # Field name made lowercase.
    emailsent = models.BooleanField(db_column='EmailSent')  # Field name made lowercase.
    emailsentdate = models.DateTimeField(db_column='EmailSentDate', blank=True, null=True)  # Field name made lowercase.
    emailschedulerinstance = models.CharField(db_column='EmailSchedulerInstance', max_length=36, blank=True, null=True)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.
    sendtoast = models.BooleanField(db_column='SendToast')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CoreMessaging_MessageRecipients'
        unique_together = (('messageid', 'userid', 'read', 'sendtoast'),)


class CoremessagingMessages(models.Model):
    messageid = models.AutoField(db_column='MessageID', primary_key=True)  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalID', blank=True, null=True)  # Field name made lowercase.
    notificationtypeid = models.ForeignKey('CoremessagingNotificationtypes', models.DO_NOTHING, db_column='NotificationTypeID', blank=True, null=True)  # Field name made lowercase.
    to = models.CharField(db_column='To', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    from_field = models.CharField(db_column='From', max_length=200, blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    subject = models.CharField(db_column='Subject', max_length=400, blank=True, null=True)  # Field name made lowercase.
    body = models.TextField(db_column='Body', blank=True, null=True)  # Field name made lowercase.
    conversationid = models.IntegerField(db_column='ConversationID', blank=True, null=True)  # Field name made lowercase.
    replyallallowed = models.NullBooleanField(db_column='ReplyAllAllowed')  # Field name made lowercase.
    senderuserid = models.IntegerField(db_column='SenderUserID', blank=True, null=True)  # Field name made lowercase.
    expirationdate = models.DateTimeField(db_column='ExpirationDate', blank=True, null=True)  # Field name made lowercase.
    context = models.CharField(db_column='Context', max_length=200, blank=True, null=True)  # Field name made lowercase.
    includedismissaction = models.NullBooleanField(db_column='IncludeDismissAction')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CoreMessaging_Messages'
        unique_together = (('messageid', 'portalid', 'notificationtypeid', 'expirationdate', 'to', 'from_field', 'subject', 'body', 'conversationid', 'replyallallowed', 'senderuserid', 'context', 'includedismissaction', 'createdbyuserid', 'createdondate', 'lastmodifiedbyuserid', 'lastmodifiedondate'),)


class CoremessagingNotificationtypeactions(models.Model):
    notificationtypeactionid = models.AutoField(db_column='NotificationTypeActionID', primary_key=True)  # Field name made lowercase.
    notificationtypeid = models.ForeignKey('CoremessagingNotificationtypes', models.DO_NOTHING, db_column='NotificationTypeID')  # Field name made lowercase.
    nameresourcekey = models.CharField(db_column='NameResourceKey', max_length=100)  # Field name made lowercase.
    descriptionresourcekey = models.CharField(db_column='DescriptionResourceKey', max_length=100, blank=True, null=True)  # Field name made lowercase.
    confirmresourcekey = models.CharField(db_column='ConfirmResourceKey', max_length=100, blank=True, null=True)  # Field name made lowercase.
    order = models.IntegerField(db_column='Order')  # Field name made lowercase.
    apicall = models.CharField(db_column='APICall', max_length=500)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CoreMessaging_NotificationTypeActions'


class CoremessagingNotificationtypes(models.Model):
    notificationtypeid = models.AutoField(db_column='NotificationTypeID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', unique=True, max_length=100)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    ttl = models.IntegerField(db_column='TTL', blank=True, null=True)  # Field name made lowercase.
    desktopmoduleid = models.ForeignKey('Desktopmodules', models.DO_NOTHING, db_column='DesktopModuleID', blank=True, null=True)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.
    istask = models.BooleanField(db_column='IsTask')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CoreMessaging_NotificationTypes'


class CoremessagingSubscriptiontypes(models.Model):
    subscriptiontypeid = models.AutoField(db_column='SubscriptionTypeId', primary_key=True)  # Field name made lowercase.
    subscriptionname = models.CharField(db_column='SubscriptionName', unique=True, max_length=50)  # Field name made lowercase.
    friendlyname = models.CharField(db_column='FriendlyName', max_length=50)  # Field name made lowercase.
    desktopmoduleid = models.IntegerField(db_column='DesktopModuleId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CoreMessaging_SubscriptionTypes'


class CoremessagingSubscriptions(models.Model):
    subscriptionid = models.AutoField(db_column='SubscriptionId', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='UserId')  # Field name made lowercase.
    portalid = models.ForeignKey('Portals', models.DO_NOTHING, db_column='PortalId', blank=True, null=True)  # Field name made lowercase.
    subscriptiontypeid = models.ForeignKey(CoremessagingSubscriptiontypes, models.DO_NOTHING, db_column='SubscriptionTypeId')  # Field name made lowercase.
    objectkey = models.CharField(db_column='ObjectKey', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objectdata = models.TextField(db_column='ObjectData', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate')  # Field name made lowercase.
    moduleid = models.ForeignKey('Modules', models.DO_NOTHING, db_column='ModuleId', blank=True, null=True)  # Field name made lowercase.
    tabid = models.IntegerField(db_column='TabId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CoreMessaging_Subscriptions'


class CoremessagingUserpreferences(models.Model):
    userpreferenceid = models.AutoField(db_column='UserPreferenceId', primary_key=True)  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserId')  # Field name made lowercase.
    messagesemailfrequency = models.IntegerField(db_column='MessagesEmailFrequency')  # Field name made lowercase.
    notificationsemailfrequency = models.IntegerField(db_column='NotificationsEmailFrequency')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CoreMessaging_UserPreferences'


class DnngoDnngalleryproFilelogs(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sliderid = models.IntegerField(db_column='SliderID')  # Field name made lowercase.
    layerid = models.IntegerField(db_column='LayerID')  # Field name made lowercase.
    fileid = models.IntegerField(db_column='FileID')  # Field name made lowercase.
    filelink = models.CharField(db_column='FileLink', max_length=512, blank=True, null=True)  # Field name made lowercase.
    options = models.TextField(db_column='Options', blank=True, null=True)  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    createuser = models.IntegerField(db_column='CreateUser')  # Field name made lowercase.
    createip = models.CharField(db_column='CreateIP', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_DNNGalleryPro_FileLogs'


class DnngoDnngalleryproFiles(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=256)  # Field name made lowercase.
    filename = models.CharField(db_column='FileName', max_length=128)  # Field name made lowercase.
    filemate = models.CharField(db_column='FileMate', max_length=32)  # Field name made lowercase.
    filepath = models.CharField(db_column='FilePath', max_length=256)  # Field name made lowercase.
    fileextension = models.CharField(db_column='FileExtension', max_length=32)  # Field name made lowercase.
    filesize = models.IntegerField(db_column='FileSize')  # Field name made lowercase.
    imagewidth = models.IntegerField(db_column='ImageWidth')  # Field name made lowercase.
    imageheight = models.IntegerField(db_column='ImageHeight')  # Field name made lowercase.
    exif = models.TextField(db_column='Exif', blank=True, null=True)  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=32)  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    extension1 = models.SmallIntegerField(db_column='Extension1')  # Field name made lowercase.
    extension2 = models.IntegerField(db_column='Extension2')  # Field name made lowercase.
    extension3 = models.CharField(db_column='Extension3', max_length=512, blank=True, null=True)  # Field name made lowercase.
    extension4 = models.TextField(db_column='Extension4', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_DNNGalleryPro_Files'


class DnngoDnngalleryproGroup(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=512, blank=True, null=True)  # Field name made lowercase.
    quotecount = models.IntegerField(db_column='QuoteCount')  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    options = models.TextField(db_column='Options', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_DNNGalleryPro_Group'


class DnngoDnngalleryproLayer(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sliderid = models.IntegerField(db_column='SliderID')  # Field name made lowercase.
    options = models.TextField(db_column='Options', blank=True, null=True)  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    createuser = models.IntegerField(db_column='CreateUser')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50)  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    per_allusers = models.SmallIntegerField(db_column='Per_AllUsers')  # Field name made lowercase.
    per_roles = models.TextField(db_column='Per_Roles', blank=True, null=True)  # Field name made lowercase.
    clicks = models.IntegerField(db_column='Clicks')  # Field name made lowercase.
    views = models.IntegerField(db_column='Views')  # Field name made lowercase.
    heats = models.IntegerField(db_column='Heats')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_DNNGalleryPro_Layer'


class DnngoDnngalleryproSlider(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    options = models.TextField(db_column='Options', blank=True, null=True)  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    createuser = models.IntegerField(db_column='CreateUser')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    starttime = models.DateTimeField(db_column='StartTime')  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='EndTime')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50)  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    per_allusers = models.SmallIntegerField(db_column='Per_AllUsers')  # Field name made lowercase.
    per_roles = models.TextField(db_column='Per_Roles', blank=True, null=True)  # Field name made lowercase.
    attribute1 = models.IntegerField(db_column='Attribute1')  # Field name made lowercase.
    attribute2 = models.TextField(db_column='Attribute2', blank=True, null=True)  # Field name made lowercase.
    extension = models.TextField(db_column='Extension', blank=True, null=True)  # Field name made lowercase.
    clicks = models.IntegerField(db_column='Clicks')  # Field name made lowercase.
    views = models.IntegerField(db_column='Views')  # Field name made lowercase.
    heats = models.IntegerField(db_column='Heats')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_DNNGalleryPro_Slider'


class DnngoDnngalleryproSliderGroup(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sliderid = models.IntegerField(db_column='SliderID')  # Field name made lowercase.
    groupid = models.IntegerField(db_column='GroupID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_DNNGalleryPro_Slider_Group'


class DnngoDnngalleryContent(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=100)  # Field name made lowercase.
    subtitle = models.CharField(db_column='Subtitle', max_length=100, blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    contenttext = models.TextField(db_column='ContentText', blank=True, null=True)  # Field name made lowercase.
    picture = models.CharField(db_column='Picture', max_length=200, blank=True, null=True)  # Field name made lowercase.
    thumbnails = models.CharField(db_column='Thumbnails', max_length=200, blank=True, null=True)  # Field name made lowercase.
    urllink = models.CharField(db_column='UrlLink', max_length=200, blank=True, null=True)  # Field name made lowercase.
    viewtype = models.SmallIntegerField(db_column='ViewType')  # Field name made lowercase.
    viewtabid = models.IntegerField(db_column='ViewTabId')  # Field name made lowercase.
    viewmoduleid = models.IntegerField(db_column='ViewModuleId')  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50)  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    urllinktype = models.SmallIntegerField(db_column='UrlLinkType')  # Field name made lowercase.
    urllinktarget = models.SmallIntegerField(db_column='UrlLinkTarget')  # Field name made lowercase.
    options = models.TextField(db_column='Options', blank=True, null=True)  # Field name made lowercase.
    starttime = models.DateTimeField(db_column='StartTime')  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='EndTime')  # Field name made lowercase.
    per_allusers = models.SmallIntegerField(db_column='Per_AllUsers')  # Field name made lowercase.
    per_roles = models.TextField(db_column='Per_Roles', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_DNNGallery_Content'


class DnngoDnngalleryContentGroup(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    contentid = models.IntegerField(db_column='ContentID')  # Field name made lowercase.
    groupid = models.IntegerField(db_column='GroupID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_DNNGallery_Content_Group'


class DnngoDnngalleryFiles(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=256)  # Field name made lowercase.
    filename = models.CharField(db_column='FileName', max_length=128)  # Field name made lowercase.
    filemate = models.CharField(db_column='FileMate', max_length=32)  # Field name made lowercase.
    filepath = models.CharField(db_column='FilePath', max_length=256)  # Field name made lowercase.
    fileextension = models.CharField(db_column='FileExtension', max_length=32)  # Field name made lowercase.
    filesize = models.IntegerField(db_column='FileSize')  # Field name made lowercase.
    imagewidth = models.IntegerField(db_column='ImageWidth')  # Field name made lowercase.
    imageheight = models.IntegerField(db_column='ImageHeight')  # Field name made lowercase.
    exif = models.TextField(db_column='Exif', blank=True, null=True)  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=32)  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    extension1 = models.SmallIntegerField(db_column='Extension1')  # Field name made lowercase.
    extension2 = models.IntegerField(db_column='Extension2')  # Field name made lowercase.
    extension3 = models.CharField(db_column='Extension3', max_length=512, blank=True, null=True)  # Field name made lowercase.
    extension4 = models.TextField(db_column='Extension4', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_DNNGallery_Files'


class DnngoDnngalleryGroup(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=512, blank=True, null=True)  # Field name made lowercase.
    quotecount = models.IntegerField(db_column='QuoteCount')  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_DNNGallery_Group'


class DnngoLayergalleryContent(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=200)  # Field name made lowercase.
    options = models.TextField(db_column='Options', blank=True, null=True)  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    starttime = models.DateTimeField(db_column='StartTime')  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='EndTime')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50)  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_LayerGallery_Content'


class DnngoLayergalleryFiles(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=256)  # Field name made lowercase.
    filename = models.CharField(db_column='FileName', max_length=128)  # Field name made lowercase.
    filemate = models.CharField(db_column='FileMate', max_length=32)  # Field name made lowercase.
    filepath = models.CharField(db_column='FilePath', max_length=256)  # Field name made lowercase.
    fileextension = models.CharField(db_column='FileExtension', max_length=32)  # Field name made lowercase.
    filesize = models.IntegerField(db_column='FileSize')  # Field name made lowercase.
    imagewidth = models.IntegerField(db_column='ImageWidth')  # Field name made lowercase.
    imageheight = models.IntegerField(db_column='ImageHeight')  # Field name made lowercase.
    exif = models.TextField(db_column='Exif', blank=True, null=True)  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=32)  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    extension1 = models.SmallIntegerField(db_column='Extension1')  # Field name made lowercase.
    extension2 = models.IntegerField(db_column='Extension2')  # Field name made lowercase.
    extension3 = models.CharField(db_column='Extension3', max_length=512, blank=True, null=True)  # Field name made lowercase.
    extension4 = models.TextField(db_column='Extension4', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_LayerGallery_Files'


class DnngoLayergalleryItem(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    contentid = models.IntegerField(db_column='ContentID')  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=512)  # Field name made lowercase.
    itemtype = models.SmallIntegerField(db_column='ItemType')  # Field name made lowercase.
    options = models.TextField(db_column='Options', blank=True, null=True)  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50)  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_LayerGallery_Item'


class DnngoLayerslider3DContent(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=512)  # Field name made lowercase.
    picture = models.CharField(db_column='Picture', max_length=512, blank=True, null=True)  # Field name made lowercase.
    urllink = models.CharField(db_column='UrlLink', max_length=512, blank=True, null=True)  # Field name made lowercase.
    urllinktarget = models.SmallIntegerField(db_column='UrlLinkTarget')  # Field name made lowercase.
    urllinktype = models.SmallIntegerField(db_column='UrlLinkType')  # Field name made lowercase.
    options = models.TextField(db_column='Options', blank=True, null=True)  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50)  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    starttime = models.DateTimeField(db_column='StartTime')  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='EndTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_LayerSlider3D_Content'


class DnngoLayerslider3DItem(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    contentid = models.IntegerField(db_column='ContentID')  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=512)  # Field name made lowercase.
    itemtype = models.SmallIntegerField(db_column='ItemType')  # Field name made lowercase.
    options = models.TextField(db_column='Options', blank=True, null=True)  # Field name made lowercase.
    picture = models.CharField(db_column='Picture', max_length=512, blank=True, null=True)  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50)  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_LayerSlider3D_Item'


class DnngoMegamenuaddonFilelogs(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sliderid = models.IntegerField(db_column='SliderID')  # Field name made lowercase.
    layerid = models.IntegerField(db_column='LayerID')  # Field name made lowercase.
    fileid = models.IntegerField(db_column='FileID')  # Field name made lowercase.
    filelink = models.CharField(db_column='FileLink', max_length=512, blank=True, null=True)  # Field name made lowercase.
    options = models.TextField(db_column='Options', blank=True, null=True)  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    createuser = models.IntegerField(db_column='CreateUser')  # Field name made lowercase.
    createip = models.CharField(db_column='CreateIP', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_MegaMenuAddon_FileLogs'


class DnngoMegamenuaddonFiles(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=256)  # Field name made lowercase.
    filename = models.CharField(db_column='FileName', max_length=128)  # Field name made lowercase.
    filemate = models.CharField(db_column='FileMate', max_length=32)  # Field name made lowercase.
    filepath = models.CharField(db_column='FilePath', max_length=256)  # Field name made lowercase.
    fileextension = models.CharField(db_column='FileExtension', max_length=32)  # Field name made lowercase.
    filesize = models.IntegerField(db_column='FileSize')  # Field name made lowercase.
    imagewidth = models.IntegerField(db_column='ImageWidth')  # Field name made lowercase.
    imageheight = models.IntegerField(db_column='ImageHeight')  # Field name made lowercase.
    exif = models.TextField(db_column='Exif', blank=True, null=True)  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=32)  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    extension1 = models.SmallIntegerField(db_column='Extension1')  # Field name made lowercase.
    extension2 = models.IntegerField(db_column='Extension2')  # Field name made lowercase.
    extension3 = models.CharField(db_column='Extension3', max_length=512, blank=True, null=True)  # Field name made lowercase.
    extension4 = models.TextField(db_column='Extension4', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_MegaMenuAddon_Files'


class DnngoMegamenuaddonGroup(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=512, blank=True, null=True)  # Field name made lowercase.
    quotecount = models.IntegerField(db_column='QuoteCount')  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_MegaMenuAddon_Group'


class DnngoMegamenuaddonLayer(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sliderid = models.IntegerField(db_column='SliderID')  # Field name made lowercase.
    options = models.TextField(db_column='Options', blank=True, null=True)  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    createuser = models.IntegerField(db_column='CreateUser')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50)  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    per_allusers = models.SmallIntegerField(db_column='Per_AllUsers')  # Field name made lowercase.
    per_roles = models.TextField(db_column='Per_Roles', blank=True, null=True)  # Field name made lowercase.
    clicks = models.IntegerField(db_column='Clicks')  # Field name made lowercase.
    views = models.IntegerField(db_column='Views')  # Field name made lowercase.
    heats = models.IntegerField(db_column='Heats')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_MegaMenuAddon_Layer'


class DnngoMegamenuaddonSlider(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    options = models.TextField(db_column='Options', blank=True, null=True)  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    createuser = models.IntegerField(db_column='CreateUser')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    starttime = models.DateTimeField(db_column='StartTime')  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='EndTime')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50)  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    per_allusers = models.SmallIntegerField(db_column='Per_AllUsers')  # Field name made lowercase.
    per_roles = models.TextField(db_column='Per_Roles', blank=True, null=True)  # Field name made lowercase.
    attribute1 = models.IntegerField(db_column='Attribute1')  # Field name made lowercase.
    attribute2 = models.TextField(db_column='Attribute2', blank=True, null=True)  # Field name made lowercase.
    extension = models.TextField(db_column='Extension', blank=True, null=True)  # Field name made lowercase.
    clicks = models.IntegerField(db_column='Clicks')  # Field name made lowercase.
    views = models.IntegerField(db_column='Views')  # Field name made lowercase.
    heats = models.IntegerField(db_column='Heats')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_MegaMenuAddon_Slider'


class DnngoMegamenuaddonSliderGroup(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sliderid = models.IntegerField(db_column='SliderID')  # Field name made lowercase.
    groupid = models.IntegerField(db_column='GroupID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_MegaMenuAddon_Slider_Group'


class DnngoMegamenuContent(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    tabid = models.IntegerField(db_column='TabID')  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=50)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=200)  # Field name made lowercase.
    contenttext = models.TextField(db_column='ContentText')  # Field name made lowercase.
    position = models.SmallIntegerField(db_column='Position')  # Field name made lowercase.
    bindtabid = models.IntegerField(db_column='BindTabID')  # Field name made lowercase.
    bindmoduleid = models.IntegerField(db_column='BindModuleID')  # Field name made lowercase.
    options = models.TextField(db_column='Options')  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=32)  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    globals_background = models.SmallIntegerField(db_column='Globals_Background')  # Field name made lowercase.
    globals_breadcrumb = models.SmallIntegerField(db_column='Globals_Breadcrumb')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_Megamenu_Content'


class DnngoMegamenuOptions(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    tabid = models.IntegerField(db_column='TabID')  # Field name made lowercase.
    tabtype = models.SmallIntegerField(db_column='TabType')  # Field name made lowercase.
    options = models.TextField(db_column='Options')  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=32)  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_Megamenu_Options'


class DnngoPhotoalbumsAlbum(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=256)  # Field name made lowercase.
    summary = models.CharField(db_column='Summary', max_length=512, blank=True, null=True)  # Field name made lowercase.
    contenttext = models.TextField(db_column='ContentText', blank=True, null=True)  # Field name made lowercase.
    photocount = models.IntegerField(db_column='PhotoCount')  # Field name made lowercase.
    albumsize = models.IntegerField(db_column='AlbumSize')  # Field name made lowercase.
    tags = models.CharField(db_column='Tags', max_length=256, blank=True, null=True)  # Field name made lowercase.
    additionalpicture = models.IntegerField(db_column='AdditionalPicture')  # Field name made lowercase.
    locationstatus = models.SmallIntegerField(db_column='LocationStatus')  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=128, blank=True, null=True)  # Field name made lowercase.
    location_x = models.CharField(db_column='Location_X', max_length=20, blank=True, null=True)  # Field name made lowercase.
    location_y = models.CharField(db_column='Location_Y', max_length=20, blank=True, null=True)  # Field name made lowercase.
    commentcount = models.IntegerField(db_column='CommentCount')  # Field name made lowercase.
    viewcount = models.IntegerField(db_column='ViewCount')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    viewstatus = models.SmallIntegerField(db_column='ViewStatus')  # Field name made lowercase.
    question = models.CharField(db_column='Question', max_length=128, blank=True, null=True)  # Field name made lowercase.
    answer = models.CharField(db_column='Answer', max_length=128, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=128, blank=True, null=True)  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    createuser = models.IntegerField(db_column='CreateUser')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    publishtime = models.DateTimeField(db_column='PublishTime')  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50)  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    searchtitle = models.CharField(db_column='SearchTitle', max_length=128, blank=True, null=True)  # Field name made lowercase.
    searchkeywords = models.CharField(db_column='SearchKeywords', max_length=256, blank=True, null=True)  # Field name made lowercase.
    searchdescription = models.CharField(db_column='SearchDescription', max_length=512, blank=True, null=True)  # Field name made lowercase.
    extension1 = models.SmallIntegerField(db_column='Extension1')  # Field name made lowercase.
    extension2 = models.IntegerField(db_column='Extension2')  # Field name made lowercase.
    extension3 = models.CharField(db_column='Extension3', max_length=512)  # Field name made lowercase.
    extension4 = models.TextField(db_column='Extension4')  # Field name made lowercase.
    options = models.TextField(db_column='Options', blank=True, null=True)  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='EndTime')  # Field name made lowercase.
    friendlyurl = models.CharField(db_column='FriendlyUrl', max_length=512, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_PhotoAlbums_Album'


class DnngoPhotoalbumsAlbumphoto(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    albumid = models.IntegerField(db_column='AlbumID')  # Field name made lowercase.
    photoid = models.IntegerField(db_column='PhotoID')  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    type = models.SmallIntegerField(db_column='Type')  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=200, blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    options = models.TextField(db_column='Options', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_PhotoAlbums_AlbumPhoto'


class DnngoPhotoalbumsCategoryRelationships(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    categoryid = models.IntegerField(db_column='CategoryID')  # Field name made lowercase.
    albumid = models.IntegerField(db_column='AlbumID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_PhotoAlbums_Category_Relationships'


class DnngoPhotoalbumsCategorys(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    parentid = models.IntegerField(db_column='ParentID')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=128)  # Field name made lowercase.
    contenttext = models.CharField(db_column='ContentText', max_length=512, blank=True, null=True)  # Field name made lowercase.
    additionalpicture = models.IntegerField(db_column='AdditionalPicture')  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    childcount = models.IntegerField(db_column='ChildCount')  # Field name made lowercase.
    articlecount = models.IntegerField(db_column='ArticleCount')  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=32)  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    friendlyurl = models.CharField(db_column='FriendlyUrl', max_length=512, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_PhotoAlbums_Categorys'


class DnngoPhotoalbumsComments(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    albumid = models.IntegerField(db_column='AlbumID')  # Field name made lowercase.
    photoid = models.IntegerField(db_column='PhotoID')  # Field name made lowercase.
    parentid = models.IntegerField(db_column='ParentID')  # Field name made lowercase.
    levelid = models.IntegerField(db_column='LevelID')  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=128)  # Field name made lowercase.
    contenttext = models.TextField(db_column='ContentText')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=64, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=32, blank=True, null=True)  # Field name made lowercase.
    website = models.CharField(db_column='WebSite', max_length=128, blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserID')  # Field name made lowercase.
    userip = models.CharField(db_column='UserIP', max_length=32)  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_PhotoAlbums_Comments'


class DnngoPhotoalbumsFilterservices(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    filtername = models.CharField(db_column='FilterName', max_length=50)  # Field name made lowercase.
    dllname = models.CharField(db_column='DllName', max_length=200)  # Field name made lowercase.
    classname = models.CharField(db_column='ClassName', max_length=200)  # Field name made lowercase.
    checkcount = models.IntegerField(db_column='CheckCount')  # Field name made lowercase.
    spamcount = models.IntegerField(db_column='SpamCount')  # Field name made lowercase.
    errorcount = models.IntegerField(db_column='ErrorCount')  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=32)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_PhotoAlbums_FilterServices'


class DnngoPhotoalbumsPhoto(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    albumid = models.IntegerField(db_column='AlbumID')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=256)  # Field name made lowercase.
    filename = models.CharField(db_column='FileName', max_length=256)  # Field name made lowercase.
    filesuffix = models.CharField(db_column='FileSuffix', max_length=50)  # Field name made lowercase.
    filesize = models.IntegerField(db_column='FileSize')  # Field name made lowercase.
    filemeta = models.CharField(db_column='FileMeta', max_length=50)  # Field name made lowercase.
    imagewidth = models.IntegerField(db_column='ImageWidth')  # Field name made lowercase.
    imageheight = models.IntegerField(db_column='ImageHeight')  # Field name made lowercase.
    exif = models.TextField(db_column='Exif', blank=True, null=True)  # Field name made lowercase.
    contenttext = models.TextField(db_column='ContentText', blank=True, null=True)  # Field name made lowercase.
    tags = models.CharField(db_column='Tags', max_length=256, blank=True, null=True)  # Field name made lowercase.
    locationstatus = models.SmallIntegerField(db_column='LocationStatus')  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=128, blank=True, null=True)  # Field name made lowercase.
    location_x = models.CharField(db_column='Location_X', max_length=20, blank=True, null=True)  # Field name made lowercase.
    location_y = models.CharField(db_column='Location_Y', max_length=20, blank=True, null=True)  # Field name made lowercase.
    viewstatus = models.SmallIntegerField(db_column='ViewStatus')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    createuser = models.IntegerField(db_column='CreateUser')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50)  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    extension1 = models.SmallIntegerField(db_column='Extension1')  # Field name made lowercase.
    extension2 = models.IntegerField(db_column='Extension2')  # Field name made lowercase.
    extension3 = models.CharField(db_column='Extension3', max_length=512)  # Field name made lowercase.
    extension4 = models.TextField(db_column='Extension4')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_PhotoAlbums_Photo'


class DnngoPhotoalbumsTags(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    contenttext = models.CharField(db_column='ContentText', max_length=50)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=512, blank=True, null=True)  # Field name made lowercase.
    quotecount = models.IntegerField(db_column='QuoteCount')  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_PhotoAlbums_Tags'


class DnngoPowerformsContent(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=100)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=256)  # Field name made lowercase.
    cultureinfo = models.CharField(db_column='CultureInfo', max_length=50)  # Field name made lowercase.
    contentvalue = models.TextField(db_column='ContentValue')  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50)  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    paymentstatus = models.CharField(db_column='PaymentStatus', max_length=200, blank=True, null=True)  # Field name made lowercase.
    paymenttime = models.DateTimeField(db_column='PaymentTime', blank=True, null=True)  # Field name made lowercase.
    paymentlink = models.CharField(db_column='PaymentLink', max_length=500, blank=True, null=True)  # Field name made lowercase.
    transactionid = models.CharField(db_column='TransactionID', max_length=500, blank=True, null=True)  # Field name made lowercase.
    verifystring = models.CharField(db_column='VerifyString', max_length=30, blank=True, null=True)  # Field name made lowercase.
    formversion = models.CharField(db_column='FormVersion', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_PowerForms_Content'


class DnngoPowerformsField(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    groupid = models.IntegerField(db_column='GroupID')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    alias = models.CharField(db_column='Alias', max_length=100)  # Field name made lowercase.
    tooltip = models.CharField(db_column='ToolTip', max_length=256, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=512, blank=True, null=True)  # Field name made lowercase.
    defaultvalue = models.TextField(db_column='DefaultValue', blank=True, null=True)  # Field name made lowercase.
    fieldtype = models.SmallIntegerField(db_column='FieldType')  # Field name made lowercase.
    direction = models.SmallIntegerField(db_column='Direction')  # Field name made lowercase.
    width = models.IntegerField(db_column='Width')  # Field name made lowercase.
    rows = models.IntegerField(db_column='Rows')  # Field name made lowercase.
    filedlist = models.TextField(db_column='FiledList', blank=True, null=True)  # Field name made lowercase.
    required = models.SmallIntegerField(db_column='Required')  # Field name made lowercase.
    verification = models.SmallIntegerField(db_column='Verification')  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50)  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    widthsuffix = models.SmallIntegerField(db_column='WidthSuffix')  # Field name made lowercase.
    listcolumn = models.IntegerField(db_column='ListColumn')  # Field name made lowercase.
    options = models.TextField(db_column='Options', blank=True, null=True)  # Field name made lowercase.
    createuser = models.IntegerField(db_column='CreateUser')  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    starttime = models.DateTimeField(db_column='StartTime')  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='EndTime')  # Field name made lowercase.
    per_allusers = models.SmallIntegerField(db_column='Per_AllUsers')  # Field name made lowercase.
    per_roles = models.TextField(db_column='Per_Roles', blank=True, null=True)  # Field name made lowercase.
    inputlength = models.IntegerField(db_column='InputLength')  # Field name made lowercase.
    equalscontrol = models.IntegerField(db_column='EqualsControl')  # Field name made lowercase.
    associatedcontrol = models.IntegerField(db_column='AssociatedControl')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_PowerForms_Field'


class DnngoPowerformsFiles(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=256)  # Field name made lowercase.
    filename = models.CharField(db_column='FileName', max_length=128)  # Field name made lowercase.
    filemate = models.CharField(db_column='FileMate', max_length=32)  # Field name made lowercase.
    filepath = models.CharField(db_column='FilePath', max_length=256)  # Field name made lowercase.
    fileextension = models.CharField(db_column='FileExtension', max_length=32)  # Field name made lowercase.
    filesize = models.IntegerField(db_column='FileSize')  # Field name made lowercase.
    imagewidth = models.IntegerField(db_column='ImageWidth')  # Field name made lowercase.
    imageheight = models.IntegerField(db_column='ImageHeight')  # Field name made lowercase.
    exif = models.TextField(db_column='Exif', blank=True, null=True)  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=32)  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    extension1 = models.SmallIntegerField(db_column='Extension1')  # Field name made lowercase.
    extension2 = models.IntegerField(db_column='Extension2')  # Field name made lowercase.
    extension3 = models.CharField(db_column='Extension3', max_length=512, blank=True, null=True)  # Field name made lowercase.
    extension4 = models.TextField(db_column='Extension4', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_PowerForms_Files'


class DnngoPowerformsGroup(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=128)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=512, blank=True, null=True)  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50)  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    options = models.TextField(db_column='Options', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_PowerForms_Group'


class DnngoPowerformsScheduler(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    senderemail = models.CharField(db_column='SenderEmail', max_length=500)  # Field name made lowercase.
    excelname = models.CharField(db_column='ExcelName', max_length=500)  # Field name made lowercase.
    enable = models.SmallIntegerField(db_column='Enable')  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50)  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_PowerForms_Scheduler'


class DnngoPowerformsTemplate(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    receiverssubject = models.CharField(db_column='ReceiversSubject', max_length=512)  # Field name made lowercase.
    receiverstemplate = models.TextField(db_column='ReceiversTemplate')  # Field name made lowercase.
    replysubject = models.CharField(db_column='ReplySubject', max_length=512)  # Field name made lowercase.
    replytemplate = models.TextField(db_column='ReplyTemplate')  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50)  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_PowerForms_Template'


class DnngoSliderrevolution3DContent(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=512)  # Field name made lowercase.
    picture = models.CharField(db_column='Picture', max_length=512, blank=True, null=True)  # Field name made lowercase.
    urllink = models.CharField(db_column='UrlLink', max_length=512, blank=True, null=True)  # Field name made lowercase.
    urllinktarget = models.SmallIntegerField(db_column='UrlLinkTarget')  # Field name made lowercase.
    urllinktype = models.SmallIntegerField(db_column='UrlLinkType')  # Field name made lowercase.
    options = models.TextField(db_column='Options', blank=True, null=True)  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50)  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    starttime = models.DateTimeField(db_column='StartTime')  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='EndTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_SliderRevolution3D_Content'


class DnngoSliderrevolution3DItem(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    contentid = models.IntegerField(db_column='ContentID')  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=512)  # Field name made lowercase.
    itemtype = models.SmallIntegerField(db_column='ItemType')  # Field name made lowercase.
    options = models.TextField(db_column='Options', blank=True, null=True)  # Field name made lowercase.
    picture = models.CharField(db_column='Picture', max_length=512, blank=True, null=True)  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50)  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_SliderRevolution3D_Item'


class DnngoXblogArticles(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=512, blank=True, null=True)  # Field name made lowercase.
    summary = models.CharField(db_column='Summary', max_length=2048, blank=True, null=True)  # Field name made lowercase.
    contenttext = models.TextField(db_column='ContentText')  # Field name made lowercase.
    additionalpicture = models.IntegerField(db_column='AdditionalPicture')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    attributionstatus = models.SmallIntegerField(db_column='AttributionStatus')  # Field name made lowercase.
    topstatus = models.SmallIntegerField(db_column='TopStatus')  # Field name made lowercase.
    tags = models.CharField(db_column='Tags', max_length=512, blank=True, null=True)  # Field name made lowercase.
    commentcount = models.IntegerField(db_column='CommentCount')  # Field name made lowercase.
    viewcount = models.IntegerField(db_column='ViewCount')  # Field name made lowercase.
    publishtime = models.DateTimeField(db_column='PublishTime')  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='EndTime', blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    createuser = models.IntegerField(db_column='CreateUser')  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50, blank=True, null=True)  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    feature = models.SmallIntegerField(db_column='Feature')  # Field name made lowercase.
    searchtitle = models.CharField(db_column='SearchTitle', max_length=512, blank=True, null=True)  # Field name made lowercase.
    searchkeywords = models.CharField(db_column='SearchKeywords', max_length=512, blank=True, null=True)  # Field name made lowercase.
    searchdescription = models.CharField(db_column='SearchDescription', max_length=512, blank=True, null=True)  # Field name made lowercase.
    options = models.TextField(db_column='Options', blank=True, null=True)  # Field name made lowercase.
    extension1 = models.SmallIntegerField(db_column='Extension1', blank=True, null=True)  # Field name made lowercase.
    extension2 = models.IntegerField(db_column='Extension2', blank=True, null=True)  # Field name made lowercase.
    extension3 = models.CharField(db_column='Extension3', max_length=512, blank=True, null=True)  # Field name made lowercase.
    extension4 = models.TextField(db_column='Extension4', blank=True, null=True)  # Field name made lowercase.
    sendsubscribe = models.SmallIntegerField(db_column='SendSubscribe')  # Field name made lowercase.
    source = models.CharField(db_column='Source', max_length=512, blank=True, null=True)  # Field name made lowercase.
    friendlyurl = models.CharField(db_column='FriendlyUrl', max_length=512, blank=True, null=True)  # Field name made lowercase.
    per_allusers = models.SmallIntegerField(db_column='Per_AllUsers')  # Field name made lowercase.
    per_roles = models.TextField(db_column='Per_Roles', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return str(self.id) + ' - ' + self.title

    class Meta:
        managed = False
        db_table = 'DNNGo_xBlog_Articles'


class DnngoXblogArticlesFiles(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    articleid = models.IntegerField(db_column='ArticleID')  # Field name made lowercase.
    multimediaid = models.IntegerField(db_column='MultimediaID')  # Field name made lowercase.
    type = models.SmallIntegerField(db_column='Type')  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=100, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=500, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_xBlog_Articles_Files'


class DnngoXblogArticlesLanguage(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=50)  # Field name made lowercase.
    articleid = models.IntegerField(db_column='ArticleID')  # Field name made lowercase.
    articlelink = models.CharField(db_column='ArticleLink', max_length=500)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    createuser = models.IntegerField(db_column='CreateUser')  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50, blank=True, null=True)  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_xBlog_Articles_Language'


class DnngoXblogCategoryRelationships(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    categoryid = models.IntegerField(db_column='CategoryID')  # Field name made lowercase.
    articleid = models.IntegerField(db_column='ArticleID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_xBlog_Category_Relationships'


class DnngoXblogCategorys(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    parentid = models.IntegerField(db_column='ParentID')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=128)  # Field name made lowercase.
    contenttext = models.CharField(db_column='ContentText', max_length=512, blank=True, null=True)  # Field name made lowercase.
    additionalpicture = models.IntegerField(db_column='AdditionalPicture')  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    childcount = models.IntegerField(db_column='ChildCount')  # Field name made lowercase.
    articlecount = models.IntegerField(db_column='ArticleCount')  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50, blank=True, null=True)  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    friendlyurl = models.CharField(db_column='FriendlyUrl', max_length=512, blank=True, null=True)  # Field name made lowercase.
    options = models.TextField(db_column='Options', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_xBlog_Categorys'


class DnngoXblogComments(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    articleid = models.IntegerField(db_column='ArticleID')  # Field name made lowercase.
    parentid = models.IntegerField(db_column='ParentID')  # Field name made lowercase.
    levelid = models.IntegerField(db_column='LevelID')  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=128)  # Field name made lowercase.
    contenttext = models.TextField(db_column='ContentText')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=64, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=32, blank=True, null=True)  # Field name made lowercase.
    createtime = models.DateTimeField(db_column='CreateTime')  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserID')  # Field name made lowercase.
    userip = models.CharField(db_column='UserIP', max_length=50, blank=True, null=True)  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    website = models.CharField(db_column='WebSite', max_length=128, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_xBlog_Comments'


class DnngoXblogFiltercustom(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    action = models.SmallIntegerField(db_column='Action')  # Field name made lowercase.
    subject = models.SmallIntegerField(db_column='Subject')  # Field name made lowercase.
    operator = models.SmallIntegerField(db_column='Operator')  # Field name made lowercase.
    filtervalue = models.CharField(db_column='FilterValue', max_length=512)  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_xBlog_FilterCustom'


class DnngoXblogFilterservices(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    filtername = models.CharField(db_column='FilterName', max_length=50)  # Field name made lowercase.
    dllname = models.CharField(db_column='DllName', max_length=200)  # Field name made lowercase.
    classname = models.CharField(db_column='ClassName', max_length=200)  # Field name made lowercase.
    checkcount = models.IntegerField(db_column='CheckCount')  # Field name made lowercase.
    spamcount = models.IntegerField(db_column='SpamCount')  # Field name made lowercase.
    errorcount = models.IntegerField(db_column='ErrorCount')  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_xBlog_FilterServices'


class DnngoXblogMultimedia(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    filename = models.CharField(db_column='FileName', max_length=128)  # Field name made lowercase.
    filemate = models.CharField(db_column='FileMate', max_length=32)  # Field name made lowercase.
    filepath = models.CharField(db_column='FilePath', max_length=256)  # Field name made lowercase.
    fileextension = models.CharField(db_column='FileExtension', max_length=32)  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50, blank=True, null=True)  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=256, blank=True, null=True)  # Field name made lowercase.
    filesize = models.IntegerField(db_column='FileSize')  # Field name made lowercase.
    imagewidth = models.IntegerField(db_column='ImageWidth')  # Field name made lowercase.
    imageheight = models.IntegerField(db_column='ImageHeight')  # Field name made lowercase.
    exif = models.TextField(db_column='Exif', blank=True, null=True)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    extension1 = models.SmallIntegerField(db_column='Extension1')  # Field name made lowercase.
    extension2 = models.IntegerField(db_column='Extension2')  # Field name made lowercase.
    extension3 = models.CharField(db_column='Extension3', max_length=512, blank=True, null=True)  # Field name made lowercase.
    extension4 = models.TextField(db_column='Extension4', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_xBlog_Multimedia'


class DnngoXblogRssfeeds(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=128)  # Field name made lowercase.
    url = models.CharField(db_column='Url', max_length=512)  # Field name made lowercase.
    activation = models.SmallIntegerField(db_column='Activation')  # Field name made lowercase.
    categories = models.IntegerField()
    author = models.IntegerField(db_column='Author')  # Field name made lowercase.
    getnum = models.IntegerField(db_column='GetNum')  # Field name made lowercase.
    errornum = models.IntegerField(db_column='ErrorNum')  # Field name made lowercase.
    getlasttime = models.DateTimeField(db_column='GetLastTime')  # Field name made lowercase.
    options = models.TextField(db_column='Options', blank=True, null=True)  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_xBlog_RssFeeds'


class DnngoXblogSubscription(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    subscriptiontype = models.SmallIntegerField(db_column='SubscriptionType')  # Field name made lowercase.
    subscriptionemail = models.CharField(db_column='SubscriptionEmail', max_length=256, blank=True, null=True)  # Field name made lowercase.
    subscriptionuserid = models.IntegerField(db_column='SubscriptionUserID')  # Field name made lowercase.
    subscriptionroleid = models.IntegerField(db_column='SubscriptionRoleID')  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    starttime = models.DateTimeField(db_column='StartTime')  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='EndTime')  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50, blank=True, null=True)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    subscriptionname = models.CharField(db_column='SubscriptionName', max_length=256, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_xBlog_Subscription'


class DnngoXblogTags(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    contenttext = models.CharField(db_column='ContentText', max_length=50)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=512, blank=True, null=True)  # Field name made lowercase.
    quotecount = models.IntegerField(db_column='QuoteCount')  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_xBlog_Tags'


class DnngoXblogTemplate(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    receiverssubject = models.CharField(db_column='ReceiversSubject', max_length=512)  # Field name made lowercase.
    receiverstemplate = models.TextField(db_column='ReceiversTemplate')  # Field name made lowercase.
    replysubject = models.CharField(db_column='ReplySubject', max_length=512)  # Field name made lowercase.
    replytemplate = models.TextField(db_column='ReplyTemplate')  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    subscriptionsubject = models.CharField(db_column='SubscriptionSubject', max_length=512, blank=True, null=True)  # Field name made lowercase.
    subscriptiontemplate = models.TextField(db_column='SubscriptionTemplate', blank=True, null=True)  # Field name made lowercase.
    subscriptionlistsubject = models.CharField(db_column='SubscriptionListSubject', max_length=512, blank=True, null=True)  # Field name made lowercase.
    subscriptionlisttemplate = models.TextField(db_column='SubscriptionListTemplate', blank=True, null=True)  # Field name made lowercase.
    subscriptionlisttemplate_items = models.TextField(db_column='SubscriptionListTemplate_Items', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_xBlog_Template'


class DnngoXblogThemeSettings(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    themename = models.CharField(db_column='ThemeName', max_length=128)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=128)  # Field name made lowercase.
    fieldname = models.CharField(db_column='FieldName', max_length=128)  # Field name made lowercase.
    fieldtype = models.SmallIntegerField(db_column='FieldType')  # Field name made lowercase.
    fielddescription = models.CharField(db_column='FieldDescription', max_length=512, blank=True, null=True)  # Field name made lowercase.
    listcollection = models.CharField(db_column='ListCollection', max_length=2048, blank=True, null=True)  # Field name made lowercase.
    listtype = models.SmallIntegerField(db_column='ListType', blank=True, null=True)  # Field name made lowercase.
    defaultvalue = models.CharField(db_column='DefaultValue', max_length=512, blank=True, null=True)  # Field name made lowercase.
    value = models.CharField(db_column='Value', max_length=2048, blank=True, null=True)  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_xBlog_Theme_Settings'


class DnngoXblogThemes(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=128)  # Field name made lowercase.
    alias = models.CharField(db_column='Alias', max_length=128)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=512, blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='Version', max_length=32)  # Field name made lowercase.
    picture = models.CharField(db_column='Picture', max_length=512, blank=True, null=True)  # Field name made lowercase.
    tags = models.CharField(db_column='Tags', max_length=128, blank=True, null=True)  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=32)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_xBlog_Themes'


class DnngoXpluginMultimedia(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=300, blank=True, null=True)  # Field name made lowercase.
    filesize = models.IntegerField(db_column='FileSize')  # Field name made lowercase.
    imagewidth = models.IntegerField(db_column='ImageWidth')  # Field name made lowercase.
    imageheight = models.IntegerField(db_column='ImageHeight')  # Field name made lowercase.
    exif = models.TextField(db_column='Exif', blank=True, null=True)  # Field name made lowercase.
    filename = models.CharField(db_column='FileName', max_length=300)  # Field name made lowercase.
    filemate = models.CharField(db_column='FileMate', max_length=32)  # Field name made lowercase.
    filepath = models.CharField(db_column='FilePath', max_length=500)  # Field name made lowercase.
    fileextension = models.CharField(db_column='FileExtension', max_length=32)  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50)  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    extension1 = models.SmallIntegerField(db_column='Extension1')  # Field name made lowercase.
    extension2 = models.IntegerField(db_column='Extension2')  # Field name made lowercase.
    extension3 = models.CharField(db_column='Extension3', max_length=512, blank=True, null=True)  # Field name made lowercase.
    extension4 = models.TextField(db_column='Extension4', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_xPlugin_Multimedia'


class DnngoXpluginRelationships(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    tabid = models.IntegerField(db_column='TabID')  # Field name made lowercase.
    fileid = models.IntegerField(db_column='FileID')  # Field name made lowercase.
    type = models.SmallIntegerField(db_column='Type')  # Field name made lowercase.
    sort = models.IntegerField(db_column='Sort')  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime')  # Field name made lowercase.
    lastuser = models.IntegerField(db_column='LastUser')  # Field name made lowercase.
    lastip = models.CharField(db_column='LastIP', max_length=50)  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNGo_xPlugin_Relationships'


class DnnproLicense(models.Model):
    licenseid = models.AutoField(db_column='LicenseID', primary_key=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=150, blank=True, null=True)  # Field name made lowercase.
    invoice = models.CharField(db_column='Invoice', max_length=150, blank=True, null=True)  # Field name made lowercase.
    expires = models.CharField(db_column='Expires', max_length=20, blank=True, null=True)  # Field name made lowercase.
    serviceenddate = models.CharField(db_column='ServiceEndDate', max_length=20, blank=True, null=True)  # Field name made lowercase.
    signature = models.CharField(db_column='Signature', max_length=60, blank=True, null=True)  # Field name made lowercase.
    hostname = models.CharField(db_column='HostName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    environment = models.IntegerField(db_column='Environment', blank=True, null=True)  # Field name made lowercase.
    additionalinfo = models.TextField(db_column='AdditionalInfo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DNNPRO_License'


class DashboardControls(models.Model):
    dashboardcontrolid = models.AutoField(db_column='DashboardControlID', primary_key=True)  # Field name made lowercase.
    dashboardcontrolkey = models.CharField(db_column='DashboardControlKey', max_length=50)  # Field name made lowercase.
    isenabled = models.BooleanField(db_column='IsEnabled')  # Field name made lowercase.
    dashboardcontrolsrc = models.CharField(db_column='DashboardControlSrc', max_length=250)  # Field name made lowercase.
    dashboardcontrollocalresources = models.CharField(db_column='DashboardControlLocalResources', max_length=250)  # Field name made lowercase.
    controllerclass = models.CharField(db_column='ControllerClass', max_length=250, blank=True, null=True)  # Field name made lowercase.
    vieworder = models.IntegerField(db_column='ViewOrder')  # Field name made lowercase.
    packageid = models.ForeignKey('Packages', models.DO_NOTHING, db_column='PackageID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dashboard_Controls'


class Desktopmodulepermission(models.Model):
    desktopmodulepermissionid = models.AutoField(db_column='DesktopModulePermissionID', primary_key=True)  # Field name made lowercase.
    portaldesktopmoduleid = models.ForeignKey('Portaldesktopmodules', models.DO_NOTHING, db_column='PortalDesktopModuleID')  # Field name made lowercase.
    permissionid = models.ForeignKey('Permission', models.DO_NOTHING, db_column='PermissionID')  # Field name made lowercase.
    allowaccess = models.BooleanField(db_column='AllowAccess')  # Field name made lowercase.
    roleid = models.ForeignKey('Roles', models.DO_NOTHING, db_column='RoleID', blank=True, null=True)  # Field name made lowercase.
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='UserID', blank=True, null=True)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DesktopModulePermission'
        unique_together = (('portaldesktopmoduleid', 'permissionid', 'roleid', 'userid', 'allowaccess'), ('userid', 'portaldesktopmoduleid', 'permissionid', 'allowaccess'), ('roleid', 'portaldesktopmoduleid', 'permissionid', 'allowaccess'),)


class Desktopmodules(models.Model):
    desktopmoduleid = models.AutoField(db_column='DesktopModuleID', primary_key=True)  # Field name made lowercase.
    friendlyname = models.CharField(db_column='FriendlyName', max_length=128)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='Version', max_length=8, blank=True, null=True)  # Field name made lowercase.
    ispremium = models.BooleanField(db_column='IsPremium')  # Field name made lowercase.
    isadmin = models.BooleanField(db_column='IsAdmin')  # Field name made lowercase.
    businesscontrollerclass = models.CharField(db_column='BusinessControllerClass', max_length=200, blank=True, null=True)  # Field name made lowercase.
    foldername = models.CharField(db_column='FolderName', max_length=128)  # Field name made lowercase.
    modulename = models.CharField(db_column='ModuleName', unique=True, max_length=128)  # Field name made lowercase.
    supportedfeatures = models.IntegerField(db_column='SupportedFeatures')  # Field name made lowercase.
    compatibleversions = models.CharField(db_column='CompatibleVersions', max_length=500, blank=True, null=True)  # Field name made lowercase.
    dependencies = models.CharField(db_column='Dependencies', max_length=400, blank=True, null=True)  # Field name made lowercase.
    permissions = models.CharField(db_column='Permissions', max_length=400, blank=True, null=True)  # Field name made lowercase.
    packageid = models.ForeignKey('Packages', models.DO_NOTHING, db_column='PackageID')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.
    contentitemid = models.IntegerField(db_column='ContentItemId')  # Field name made lowercase.
    shareable = models.IntegerField(db_column='Shareable')  # Field name made lowercase.
    adminpage = models.CharField(db_column='AdminPage', max_length=128, blank=True, null=True)  # Field name made lowercase.
    hostpage = models.CharField(db_column='HostPage', max_length=128, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DesktopModules'


class Documents(models.Model):
    itemid = models.AutoField(db_column='ItemID', primary_key=True)  # Field name made lowercase.
    moduleid = models.ForeignKey('Modules', models.DO_NOTHING, db_column='ModuleID')  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    url = models.CharField(db_column='URL', max_length=250, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=150, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    ownedbyuserid = models.IntegerField(db_column='OwnedByUserID', blank=True, null=True)  # Field name made lowercase.
    modifiedbyuserid = models.IntegerField(db_column='ModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    modifieddate = models.DateTimeField(db_column='ModifiedDate', blank=True, null=True)  # Field name made lowercase.
    sortorderindex = models.IntegerField(db_column='SortOrderIndex', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.
    forcedownload = models.NullBooleanField(db_column='ForceDownload')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Documents'


class Documentssettings(models.Model):
    moduleid = models.OneToOneField('Modules', models.DO_NOTHING, db_column='ModuleID', primary_key=True)  # Field name made lowercase.
    showtitlelink = models.NullBooleanField(db_column='ShowTitleLink')  # Field name made lowercase.
    sortorder = models.CharField(db_column='SortOrder', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    displaycolumns = models.CharField(db_column='DisplayColumns', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    usecategorieslist = models.NullBooleanField(db_column='UseCategoriesList')  # Field name made lowercase.
    defaultfolder = models.CharField(db_column='DefaultFolder', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    categorieslistname = models.CharField(db_column='CategoriesListName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    allowusersort = models.NullBooleanField(db_column='AllowUserSort')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DocumentsSettings'


class Eventlog(models.Model):
    logguid = models.CharField(db_column='LogGUID', max_length=36)  # Field name made lowercase.
    logtypekey = models.ForeignKey('Eventlogtypes', models.DO_NOTHING, db_column='LogTypeKey')  # Field name made lowercase.
    logconfigid = models.ForeignKey('Eventlogconfig', models.DO_NOTHING, db_column='LogConfigID', blank=True, null=True)  # Field name made lowercase.
    loguserid = models.IntegerField(db_column='LogUserID', blank=True, null=True)  # Field name made lowercase.
    logusername = models.CharField(db_column='LogUserName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    logportalid = models.IntegerField(db_column='LogPortalID', blank=True, null=True)  # Field name made lowercase.
    logportalname = models.CharField(db_column='LogPortalName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    logcreatedate = models.DateTimeField(db_column='LogCreateDate')  # Field name made lowercase.
    logservername = models.CharField(db_column='LogServerName', max_length=50)  # Field name made lowercase.
    logproperties = models.TextField(db_column='LogProperties', blank=True, null=True)  # Field name made lowercase.
    lognotificationpending = models.NullBooleanField(db_column='LogNotificationPending')  # Field name made lowercase.
    logeventid = models.BigAutoField(db_column='LogEventID', primary_key=True)  # Field name made lowercase.
    exceptionhash = models.CharField(db_column='ExceptionHash', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EventLog'


class Eventlogconfig(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    logtypekey = models.ForeignKey('Eventlogtypes', models.DO_NOTHING, db_column='LogTypeKey', blank=True, null=True)  # Field name made lowercase.
    logtypeportalid = models.IntegerField(db_column='LogTypePortalID', blank=True, null=True)  # Field name made lowercase.
    loggingisactive = models.BooleanField(db_column='LoggingIsActive')  # Field name made lowercase.
    keepmostrecent = models.IntegerField(db_column='KeepMostRecent')  # Field name made lowercase.
    emailnotificationisactive = models.BooleanField(db_column='EmailNotificationIsActive')  # Field name made lowercase.
    notificationthreshold = models.IntegerField(db_column='NotificationThreshold', blank=True, null=True)  # Field name made lowercase.
    notificationthresholdtime = models.IntegerField(db_column='NotificationThresholdTime', blank=True, null=True)  # Field name made lowercase.
    notificationthresholdtimetype = models.IntegerField(db_column='NotificationThresholdTimeType', blank=True, null=True)  # Field name made lowercase.
    mailfromaddress = models.CharField(db_column='MailFromAddress', max_length=50)  # Field name made lowercase.
    mailtoaddress = models.CharField(db_column='MailToAddress', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EventLogConfig'
        unique_together = (('logtypekey', 'logtypeportalid'),)


class Eventlogtypes(models.Model):
    logtypekey = models.CharField(db_column='LogTypeKey', primary_key=True, max_length=35)  # Field name made lowercase.
    logtypefriendlyname = models.CharField(db_column='LogTypeFriendlyName', max_length=50)  # Field name made lowercase.
    logtypedescription = models.CharField(db_column='LogTypeDescription', max_length=128)  # Field name made lowercase.
    logtypeowner = models.CharField(db_column='LogTypeOwner', max_length=100)  # Field name made lowercase.
    logtypecssclass = models.CharField(db_column='LogTypeCSSClass', max_length=40)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EventLogTypes'


class Eventqueue(models.Model):
    eventmessageid = models.AutoField(db_column='EventMessageID', primary_key=True)  # Field name made lowercase.
    eventname = models.CharField(db_column='EventName', max_length=100)  # Field name made lowercase.
    priority = models.IntegerField(db_column='Priority')  # Field name made lowercase.
    processortype = models.CharField(db_column='ProcessorType', max_length=250)  # Field name made lowercase.
    processorcommand = models.CharField(db_column='ProcessorCommand', max_length=250)  # Field name made lowercase.
    body = models.CharField(db_column='Body', max_length=250)  # Field name made lowercase.
    sender = models.CharField(db_column='Sender', max_length=250)  # Field name made lowercase.
    subscriber = models.CharField(db_column='Subscriber', max_length=100)  # Field name made lowercase.
    authorizedroles = models.CharField(db_column='AuthorizedRoles', max_length=250)  # Field name made lowercase.
    exceptionmessage = models.CharField(db_column='ExceptionMessage', max_length=250)  # Field name made lowercase.
    sentdate = models.DateTimeField(db_column='SentDate')  # Field name made lowercase.
    expirationdate = models.DateTimeField(db_column='ExpirationDate')  # Field name made lowercase.
    attributes = models.TextField(db_column='Attributes')  # Field name made lowercase.
    iscomplete = models.BooleanField(db_column='IsComplete')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EventQueue'


class Events(models.Model):
    eventid = models.AutoField(db_column='EventID', primary_key=True)  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleID')  # Field name made lowercase.
    eventdatebegin = models.DateTimeField(db_column='EventDateBegin', blank=True, null=True)  # Field name made lowercase.
    eventdateend = models.DateTimeField(db_column='EventDateEnd', blank=True, null=True)  # Field name made lowercase.
    eventtimebegin = models.DateTimeField(db_column='EventTimeBegin')  # Field name made lowercase.
    duration = models.IntegerField(db_column='Duration')  # Field name made lowercase.
    eventname = models.CharField(db_column='EventName', max_length=100)  # Field name made lowercase.
    eventdesc = models.TextField(db_column='EventDesc', blank=True, null=True)  # Field name made lowercase.
    importance = models.IntegerField(db_column='Importance')  # Field name made lowercase.
    repeattype = models.CharField(db_column='RepeatType', max_length=10, blank=True, null=True)  # Field name made lowercase.
    every = models.CharField(db_column='Every', max_length=10, blank=True, null=True)  # Field name made lowercase.
    period = models.CharField(db_column='Period', max_length=50, blank=True, null=True)  # Field name made lowercase.
    reminder = models.CharField(db_column='Reminder', max_length=2048, blank=True, null=True)  # Field name made lowercase.
    notify = models.CharField(db_column='Notify', max_length=2048, blank=True, null=True)  # Field name made lowercase.
    createdbyid = models.IntegerField(db_column='CreatedByID')  # Field name made lowercase.
    approved = models.BooleanField(db_column='Approved')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalID')  # Field name made lowercase.
    signups = models.BooleanField(db_column='Signups')  # Field name made lowercase.
    maxenrollment = models.IntegerField(db_column='MaxEnrollment')  # Field name made lowercase.
    enrollroleid = models.IntegerField(db_column='EnrollRoleID', blank=True, null=True)  # Field name made lowercase.
    enrollfee = models.DecimalField(db_column='EnrollFee', max_digits=19, decimal_places=4)  # Field name made lowercase.
    enrolltype = models.CharField(db_column='EnrollType', max_length=10)  # Field name made lowercase.
    paypalaccount = models.CharField(db_column='PayPalAccount', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cancelled = models.BooleanField(db_column='Cancelled')  # Field name made lowercase.
    imageurl = models.CharField(db_column='ImageURL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    imagetype = models.CharField(db_column='ImageType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    imagewidth = models.IntegerField(db_column='ImageWidth', blank=True, null=True)  # Field name made lowercase.
    imageheight = models.IntegerField(db_column='ImageHeight', blank=True, null=True)  # Field name made lowercase.
    imagedisplay = models.BooleanField(db_column='ImageDisplay')  # Field name made lowercase.
    location = models.ForeignKey('Eventslocation', models.DO_NOTHING, db_column='Location', blank=True, null=True)  # Field name made lowercase.
    category = models.ForeignKey('Eventscategory', models.DO_NOTHING, db_column='Category', blank=True, null=True)  # Field name made lowercase.
    sendreminder = models.BooleanField(db_column='SendReminder')  # Field name made lowercase.
    remindertime = models.IntegerField(db_column='ReminderTime')  # Field name made lowercase.
    remindertimemeasurement = models.CharField(db_column='ReminderTimeMeasurement', max_length=2)  # Field name made lowercase.
    reminderfrom = models.CharField(db_column='ReminderFrom', max_length=100)  # Field name made lowercase.
    searchsubmitted = models.BooleanField(db_column='SearchSubmitted')  # Field name made lowercase.
    customfield1 = models.CharField(db_column='CustomField1', max_length=100, blank=True, null=True)  # Field name made lowercase.
    customfield2 = models.CharField(db_column='CustomField2', max_length=100, blank=True, null=True)  # Field name made lowercase.
    lastupdatedat = models.DateTimeField(db_column='LastUpdatedAt')  # Field name made lowercase.
    originaldatebegin = models.DateTimeField(db_column='OriginalDateBegin')  # Field name made lowercase.
    lastupdatedid = models.IntegerField(db_column='LastUpdatedID')  # Field name made lowercase.
    ownerid = models.IntegerField(db_column='OwnerID')  # Field name made lowercase.
    enrolllistview = models.BooleanField(db_column='EnrollListView')  # Field name made lowercase.
    neweventemailsent = models.BooleanField(db_column='NewEventEmailSent')  # Field name made lowercase.
    displayenddate = models.BooleanField(db_column='DisplayEndDate')  # Field name made lowercase.
    alldayevent = models.BooleanField(db_column='AllDayEvent')  # Field name made lowercase.
    recurmasterid = models.ForeignKey('Eventsrecurmaster', models.DO_NOTHING, db_column='RecurMasterID')  # Field name made lowercase.
    detailpage = models.BooleanField(db_column='DetailPage')  # Field name made lowercase.
    detailurl = models.CharField(db_column='DetailURL', max_length=200, blank=True, null=True)  # Field name made lowercase.
    detailnewwin = models.BooleanField(db_column='DetailNewWin')  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate')  # Field name made lowercase.
    allowanonenroll = models.BooleanField(db_column='AllowAnonEnroll')  # Field name made lowercase.
    contentitemid = models.IntegerField(db_column='ContentItemId', blank=True, null=True)  # Field name made lowercase.
    journalitem = models.BooleanField(db_column='JournalItem')  # Field name made lowercase.
    summary = models.TextField(db_column='Summary', blank=True, null=True)  # Field name made lowercase.
    sequence = models.IntegerField(db_column='Sequence')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Events'


class Eventscategory(models.Model):
    portalid = models.ForeignKey('Portals', models.DO_NOTHING, db_column='PortalID')  # Field name made lowercase.
    category = models.AutoField(db_column='Category', primary_key=True)  # Field name made lowercase.
    categoryname = models.CharField(db_column='CategoryName', max_length=50)  # Field name made lowercase.
    color = models.CharField(db_column='Color', max_length=10, blank=True, null=True)  # Field name made lowercase.
    fontcolor = models.CharField(db_column='FontColor', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EventsCategory'


class Eventslocation(models.Model):
    portalid = models.ForeignKey('Portals', models.DO_NOTHING, db_column='PortalID')  # Field name made lowercase.
    location = models.AutoField(db_column='Location', primary_key=True)  # Field name made lowercase.
    locationname = models.CharField(db_column='LocationName', max_length=50)  # Field name made lowercase.
    mapurl = models.CharField(db_column='MapURL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    street = models.CharField(db_column='Street', max_length=50, blank=True, null=True)  # Field name made lowercase.
    postalcode = models.CharField(db_column='PostalCode', max_length=50, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=50, blank=True, null=True)  # Field name made lowercase.
    region = models.CharField(db_column='Region', max_length=50, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EventsLocation'


class Eventsmaster(models.Model):
    masterid = models.AutoField(db_column='MasterID', primary_key=True)  # Field name made lowercase.
    moduleid = models.ForeignKey('Modules', models.DO_NOTHING, db_column='ModuleID')  # Field name made lowercase.
    subeventid = models.IntegerField(db_column='SubEventID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EventsMaster'
        unique_together = (('masterid', 'subeventid'),)


class Eventsnotification(models.Model):
    notificationid = models.AutoField(db_column='NotificationID', primary_key=True)  # Field name made lowercase.
    eventid = models.ForeignKey(Events, models.DO_NOTHING, db_column='EventID')  # Field name made lowercase.
    portalaliasid = models.IntegerField(db_column='PortalAliasID')  # Field name made lowercase.
    useremail = models.CharField(db_column='UserEmail', max_length=50)  # Field name made lowercase.
    notificationsent = models.BooleanField(db_column='NotificationSent')  # Field name made lowercase.
    notifybydatetime = models.DateTimeField(db_column='NotifyByDateTime')  # Field name made lowercase.
    eventtimebegin = models.DateTimeField(db_column='EventTimeBegin')  # Field name made lowercase.
    notifylanguage = models.CharField(db_column='NotifyLanguage', max_length=10)  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleID')  # Field name made lowercase.
    tabid = models.IntegerField(db_column='TabID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EventsNotification'
        unique_together = (('eventid', 'useremail', 'eventtimebegin'),)


class Eventspperrorlog(models.Model):
    paypalid = models.AutoField(db_column='PayPalID', primary_key=True)  # Field name made lowercase.
    signupid = models.ForeignKey('Eventssignups', models.DO_NOTHING, db_column='SignupID')  # Field name made lowercase.
    paypalstatus = models.CharField(db_column='PayPalStatus', max_length=50, blank=True, null=True)  # Field name made lowercase.
    paypalreason = models.CharField(db_column='PayPalReason', max_length=100, blank=True, null=True)  # Field name made lowercase.
    paypaltransid = models.CharField(db_column='PayPalTransID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    paypalpayerid = models.CharField(db_column='PayPalPayerID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    paypalpayerstatus = models.CharField(db_column='PayPalPayerStatus', max_length=50, blank=True, null=True)  # Field name made lowercase.
    paypalrecieveremail = models.CharField(db_column='PayPalRecieverEmail', max_length=100, blank=True, null=True)  # Field name made lowercase.
    paypaluseremail = models.CharField(db_column='PayPalUserEmail', max_length=100, blank=True, null=True)  # Field name made lowercase.
    paypalpayeremail = models.CharField(db_column='PayPalPayerEmail', max_length=100, blank=True, null=True)  # Field name made lowercase.
    paypalfirstname = models.CharField(db_column='PayPalFirstName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    paypallastname = models.CharField(db_column='PayPalLastName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    paypaladdress = models.CharField(db_column='PayPalAddress', max_length=100, blank=True, null=True)  # Field name made lowercase.
    paypalcity = models.CharField(db_column='PayPalCity', max_length=50, blank=True, null=True)  # Field name made lowercase.
    paypalstate = models.CharField(db_column='PayPalState', max_length=25, blank=True, null=True)  # Field name made lowercase.
    paypalzip = models.CharField(db_column='PayPalZip', max_length=25, blank=True, null=True)  # Field name made lowercase.
    paypalcountry = models.CharField(db_column='PayPalCountry', max_length=25, blank=True, null=True)  # Field name made lowercase.
    paypalcurrency = models.CharField(db_column='PayPalCurrency', max_length=25, blank=True, null=True)  # Field name made lowercase.
    paypalpaymentdate = models.DateTimeField(db_column='PayPalPaymentDate', blank=True, null=True)  # Field name made lowercase.
    paypalamount = models.DecimalField(db_column='PayPalAmount', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    paypalfee = models.DecimalField(db_column='PayPalFee', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EventsPPErrorLog'


class Eventsrecurmaster(models.Model):
    recurmasterid = models.AutoField(db_column='RecurMasterID', primary_key=True)  # Field name made lowercase.
    moduleid = models.ForeignKey('Modules', models.DO_NOTHING, db_column='ModuleID')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalID')  # Field name made lowercase.
    rrule = models.CharField(db_column='RRULE', max_length=1000)  # Field name made lowercase.
    dtstart = models.DateTimeField(db_column='DTSTART')  # Field name made lowercase.
    duration = models.CharField(db_column='Duration', max_length=50)  # Field name made lowercase.
    until = models.DateTimeField(db_column='Until')  # Field name made lowercase.
    eventname = models.CharField(db_column='EventName', max_length=100)  # Field name made lowercase.
    eventdesc = models.TextField(db_column='EventDesc', blank=True, null=True)  # Field name made lowercase.
    importance = models.IntegerField(db_column='Importance')  # Field name made lowercase.
    reminder = models.CharField(db_column='Reminder', max_length=2048, blank=True, null=True)  # Field name made lowercase.
    notify = models.CharField(db_column='Notify', max_length=2048, blank=True, null=True)  # Field name made lowercase.
    approved = models.BooleanField(db_column='Approved')  # Field name made lowercase.
    signups = models.BooleanField(db_column='Signups')  # Field name made lowercase.
    maxenrollment = models.IntegerField(db_column='MaxEnrollment')  # Field name made lowercase.
    enrollroleid = models.IntegerField(db_column='EnrollRoleID', blank=True, null=True)  # Field name made lowercase.
    enrollfee = models.DecimalField(db_column='EnrollFee', max_digits=19, decimal_places=4)  # Field name made lowercase.
    enrolltype = models.CharField(db_column='EnrollType', max_length=10)  # Field name made lowercase.
    paypalaccount = models.CharField(db_column='PayPalAccount', max_length=100, blank=True, null=True)  # Field name made lowercase.
    imageurl = models.CharField(db_column='ImageURL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    imagetype = models.CharField(db_column='ImageType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    imagewidth = models.IntegerField(db_column='ImageWidth', blank=True, null=True)  # Field name made lowercase.
    imageheight = models.IntegerField(db_column='ImageHeight', blank=True, null=True)  # Field name made lowercase.
    imagedisplay = models.BooleanField(db_column='ImageDisplay')  # Field name made lowercase.
    location = models.ForeignKey(Eventslocation, models.DO_NOTHING, db_column='Location', blank=True, null=True)  # Field name made lowercase.
    category = models.ForeignKey(Eventscategory, models.DO_NOTHING, db_column='Category', blank=True, null=True)  # Field name made lowercase.
    sendreminder = models.BooleanField(db_column='SendReminder')  # Field name made lowercase.
    remindertime = models.IntegerField(db_column='ReminderTime')  # Field name made lowercase.
    remindertimemeasurement = models.CharField(db_column='ReminderTimeMeasurement', max_length=2)  # Field name made lowercase.
    reminderfrom = models.CharField(db_column='ReminderFrom', max_length=100)  # Field name made lowercase.
    customfield1 = models.CharField(db_column='CustomField1', max_length=100, blank=True, null=True)  # Field name made lowercase.
    customfield2 = models.CharField(db_column='CustomField2', max_length=100, blank=True, null=True)  # Field name made lowercase.
    enrolllistview = models.BooleanField(db_column='EnrollListView')  # Field name made lowercase.
    displayenddate = models.BooleanField(db_column='DisplayEndDate')  # Field name made lowercase.
    alldayevent = models.BooleanField(db_column='AllDayEvent')  # Field name made lowercase.
    ownerid = models.IntegerField(db_column='OwnerID')  # Field name made lowercase.
    culturename = models.CharField(db_column='CultureName', max_length=10)  # Field name made lowercase.
    createdbyid = models.IntegerField(db_column='CreatedByID')  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate')  # Field name made lowercase.
    updatedbyid = models.IntegerField(db_column='UpdatedByID')  # Field name made lowercase.
    updateddate = models.DateTimeField(db_column='UpdatedDate')  # Field name made lowercase.
    detailpage = models.BooleanField(db_column='DetailPage')  # Field name made lowercase.
    detailurl = models.CharField(db_column='DetailURL', max_length=200, blank=True, null=True)  # Field name made lowercase.
    detailnewwin = models.BooleanField(db_column='DetailNewWin')  # Field name made lowercase.
    eventtimezoneid = models.CharField(db_column='EventTimeZoneId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    allowanonenroll = models.BooleanField(db_column='AllowAnonEnroll')  # Field name made lowercase.
    contentitemid = models.IntegerField(db_column='ContentItemId', blank=True, null=True)  # Field name made lowercase.
    socialgroupid = models.ForeignKey('Roles', models.DO_NOTHING, db_column='SocialGroupId', blank=True, null=True)  # Field name made lowercase.
    socialuserid = models.ForeignKey('Users', models.DO_NOTHING, db_column='SocialUserId', blank=True, null=True)  # Field name made lowercase.
    summary = models.TextField(db_column='Summary', blank=True, null=True)  # Field name made lowercase.
    sequence = models.IntegerField(db_column='Sequence')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EventsRecurMaster'


class Eventssignups(models.Model):
    signupid = models.AutoField(db_column='SignupID', primary_key=True)  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleID')  # Field name made lowercase.
    eventid = models.ForeignKey(Events, models.DO_NOTHING, db_column='EventID')  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserID')  # Field name made lowercase.
    approved = models.BooleanField(db_column='Approved')  # Field name made lowercase.
    paypalstatus = models.CharField(db_column='PayPalStatus', max_length=50, blank=True, null=True)  # Field name made lowercase.
    paypalreason = models.CharField(db_column='PayPalReason', max_length=100, blank=True, null=True)  # Field name made lowercase.
    paypaltransid = models.CharField(db_column='PayPalTransID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    paypalpayerid = models.CharField(db_column='PayPalPayerID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    paypalpayerstatus = models.CharField(db_column='PayPalPayerStatus', max_length=50, blank=True, null=True)  # Field name made lowercase.
    paypalrecieveremail = models.CharField(db_column='PayPalRecieverEmail', max_length=100, blank=True, null=True)  # Field name made lowercase.
    paypaluseremail = models.CharField(db_column='PayPalUserEmail', max_length=100, blank=True, null=True)  # Field name made lowercase.
    paypalpayeremail = models.CharField(db_column='PayPalPayerEmail', max_length=100, blank=True, null=True)  # Field name made lowercase.
    paypalfirstname = models.CharField(db_column='PayPalFirstName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    paypallastname = models.CharField(db_column='PayPalLastName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    paypaladdress = models.CharField(db_column='PayPalAddress', max_length=100, blank=True, null=True)  # Field name made lowercase.
    paypalcity = models.CharField(db_column='PayPalCity', max_length=50, blank=True, null=True)  # Field name made lowercase.
    paypalstate = models.CharField(db_column='PayPalState', max_length=25, blank=True, null=True)  # Field name made lowercase.
    paypalzip = models.CharField(db_column='PayPalZip', max_length=25, blank=True, null=True)  # Field name made lowercase.
    paypalcountry = models.CharField(db_column='PayPalCountry', max_length=25, blank=True, null=True)  # Field name made lowercase.
    paypalcurrency = models.CharField(db_column='PayPalCurrency', max_length=25, blank=True, null=True)  # Field name made lowercase.
    paypalpaymentdate = models.DateTimeField(db_column='PayPalPaymentDate', blank=True, null=True)  # Field name made lowercase.
    paypalamount = models.DecimalField(db_column='PayPalAmount', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    paypalfee = models.DecimalField(db_column='PayPalFee', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    noenrolees = models.IntegerField(db_column='NoEnrolees')  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    anonemail = models.CharField(db_column='AnonEmail', max_length=256, blank=True, null=True)  # Field name made lowercase.
    anonname = models.CharField(db_column='AnonName', max_length=128, blank=True, null=True)  # Field name made lowercase.
    anontelephone = models.CharField(db_column='AnonTelephone', max_length=128, blank=True, null=True)  # Field name made lowercase.
    anonculture = models.CharField(db_column='AnonCulture', max_length=10, blank=True, null=True)  # Field name made lowercase.
    anontimezoneid = models.CharField(db_column='AnonTimeZoneId', max_length=100, blank=True, null=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    company = models.CharField(db_column='Company', max_length=50, blank=True, null=True)  # Field name made lowercase.
    jobtitle = models.CharField(db_column='JobTitle', max_length=50, blank=True, null=True)  # Field name made lowercase.
    referencenumber = models.CharField(db_column='ReferenceNumber', max_length=50, blank=True, null=True)  # Field name made lowercase.
    street = models.CharField(db_column='Street', max_length=50, blank=True, null=True)  # Field name made lowercase.
    postalcode = models.CharField(db_column='PostalCode', max_length=50, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=50, blank=True, null=True)  # Field name made lowercase.
    region = models.CharField(db_column='Region', max_length=50, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EventsSignups'
        unique_together = (('moduleid', 'eventid', 'userid', 'anonemail'),)


class Eventssubscription(models.Model):
    subscriptionid = models.AutoField(db_column='SubscriptionID', primary_key=True)  # Field name made lowercase.
    moduleid = models.ForeignKey('Modules', models.DO_NOTHING, db_column='ModuleID')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalID')  # Field name made lowercase.
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='UserID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EventsSubscription'


class Exceptionevents(models.Model):
    logeventid = models.OneToOneField(Eventlog, models.DO_NOTHING, db_column='LogEventID', primary_key=True)  # Field name made lowercase.
    assemblyversion = models.CharField(db_column='AssemblyVersion', max_length=20)  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId', blank=True, null=True)  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserId', blank=True, null=True)  # Field name made lowercase.
    tabid = models.IntegerField(db_column='TabId', blank=True, null=True)  # Field name made lowercase.
    rawurl = models.CharField(db_column='RawUrl', max_length=260, blank=True, null=True)  # Field name made lowercase.
    referrer = models.CharField(db_column='Referrer', max_length=260, blank=True, null=True)  # Field name made lowercase.
    useragent = models.CharField(db_column='UserAgent', max_length=260, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ExceptionEvents'


class Exceptions(models.Model):
    exceptionhash = models.CharField(db_column='ExceptionHash', primary_key=True, max_length=100)  # Field name made lowercase.
    message = models.CharField(db_column='Message', max_length=500)  # Field name made lowercase.
    stacktrace = models.TextField(db_column='StackTrace', blank=True, null=True)  # Field name made lowercase.
    innermessage = models.CharField(db_column='InnerMessage', max_length=500, blank=True, null=True)  # Field name made lowercase.
    innerstacktrace = models.TextField(db_column='InnerStackTrace', blank=True, null=True)  # Field name made lowercase.
    source = models.CharField(db_column='Source', max_length=500, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Exceptions'


class Extensionurlproviderconfiguration(models.Model):
    extensionurlproviderid = models.IntegerField(db_column='ExtensionUrlProviderID', primary_key=True)  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ExtensionUrlProviderConfiguration'
        unique_together = (('extensionurlproviderid', 'portalid'),)


class Extensionurlprovidersetting(models.Model):
    extensionurlproviderid = models.IntegerField(db_column='ExtensionUrlProviderID', primary_key=True)  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalID')  # Field name made lowercase.
    settingname = models.CharField(db_column='SettingName', max_length=100)  # Field name made lowercase.
    settingvalue = models.CharField(db_column='SettingValue', max_length=2000)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ExtensionUrlProviderSetting'
        unique_together = (('extensionurlproviderid', 'portalid', 'settingname'),)


class Extensionurlprovidertab(models.Model):
    extensionurlproviderid = models.IntegerField(db_column='ExtensionUrlProviderID', primary_key=True)  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalID')  # Field name made lowercase.
    tabid = models.IntegerField(db_column='TabID')  # Field name made lowercase.
    isactive = models.BooleanField(db_column='IsActive')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ExtensionUrlProviderTab'
        unique_together = (('extensionurlproviderid', 'portalid', 'tabid'),)


class Extensionurlproviders(models.Model):
    extensionurlproviderid = models.AutoField(db_column='ExtensionUrlProviderID', primary_key=True)  # Field name made lowercase.
    providername = models.CharField(db_column='ProviderName', max_length=150)  # Field name made lowercase.
    providertype = models.CharField(db_column='ProviderType', max_length=1000)  # Field name made lowercase.
    settingscontrolsrc = models.CharField(db_column='SettingsControlSrc', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    isactive = models.BooleanField(db_column='IsActive')  # Field name made lowercase.
    rewriteallurls = models.BooleanField(db_column='RewriteAllUrls')  # Field name made lowercase.
    redirectallurls = models.BooleanField(db_column='RedirectAllUrls')  # Field name made lowercase.
    replaceallurls = models.BooleanField(db_column='ReplaceAllUrls')  # Field name made lowercase.
    desktopmoduleid = models.IntegerField(db_column='DesktopModuleId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ExtensionUrlProviders'


class Faqs(models.Model):
    itemid = models.AutoField(db_column='ItemID', primary_key=True)  # Field name made lowercase.
    moduleid = models.ForeignKey('Modules', models.DO_NOTHING, db_column='ModuleID')  # Field name made lowercase.
    createdbyuser = models.CharField(db_column='CreatedByUser', max_length=100, blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate')  # Field name made lowercase.
    question = models.CharField(db_column='Question', max_length=400)  # Field name made lowercase.
    answer = models.TextField(db_column='Answer', blank=True, null=True)  # Field name made lowercase.
    categoryid = models.IntegerField(db_column='CategoryId', blank=True, null=True)  # Field name made lowercase.
    datemodified = models.DateTimeField(db_column='DateModified')  # Field name made lowercase.
    viewcount = models.IntegerField(db_column='ViewCount')  # Field name made lowercase.
    vieworder = models.IntegerField(db_column='ViewOrder')  # Field name made lowercase.
    faqhide = models.BooleanField(db_column='FaqHide')  # Field name made lowercase.
    publishdate = models.DateTimeField(db_column='PublishDate', blank=True, null=True)  # Field name made lowercase.
    expiredate = models.DateTimeField(db_column='ExpireDate', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return str(self.itemid) + ' - ' + self.question

    class Meta:
        managed = False
        db_table = 'FAQs'


class Faqscategory(models.Model):
    faqcategoryid = models.AutoField(db_column='FaqCategoryId', primary_key=True)  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    faqcategoryname = models.CharField(db_column='FaqCategoryName', max_length=100)  # Field name made lowercase.
    faqcategorydescription = models.CharField(db_column='FaqCategoryDescription', max_length=250)  # Field name made lowercase.
    faqcategoryparentid = models.IntegerField(db_column='FaqCategoryParentId', blank=True, null=True)  # Field name made lowercase.
    vieworder = models.IntegerField(db_column='ViewOrder')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FAQsCategory'


class Feedback(models.Model):
    moduleid = models.ForeignKey('Modules', models.DO_NOTHING, db_column='ModuleID')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status')  # Field name made lowercase.
    subject = models.CharField(db_column='Subject', max_length=200, blank=True, null=True)  # Field name made lowercase.
    senderemail = models.CharField(db_column='SenderEmail', max_length=256)  # Field name made lowercase.
    approvedby = models.IntegerField(db_column='ApprovedBy', blank=True, null=True)  # Field name made lowercase.
    message = models.TextField(db_column='Message')  # Field name made lowercase.
    createdondateserver = models.DateTimeField(db_column='CreatedOnDateServer')  # Field name made lowercase.
    feedbackid = models.AutoField(db_column='FeedbackID', primary_key=True)  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalID')  # Field name made lowercase.
    categoryid = models.CharField(db_column='CategoryID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    sendername = models.CharField(db_column='SenderName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    publishedondate = models.DateTimeField(db_column='PublishedOnDate', blank=True, null=True)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    senderstreet = models.CharField(db_column='SenderStreet', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sendercity = models.CharField(db_column='SenderCity', max_length=50, blank=True, null=True)  # Field name made lowercase.
    senderregion = models.CharField(db_column='SenderRegion', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sendercountry = models.CharField(db_column='SenderCountry', max_length=50, blank=True, null=True)  # Field name made lowercase.
    senderpostalcode = models.CharField(db_column='SenderPostalCode', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sendertelephone = models.CharField(db_column='SenderTelephone', max_length=20, blank=True, null=True)  # Field name made lowercase.
    senderremoteaddr = models.CharField(db_column='SenderRemoteAddr', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate')  # Field name made lowercase.
    referrer = models.CharField(db_column='Referrer', max_length=255, blank=True, null=True)  # Field name made lowercase.
    useragent = models.CharField(db_column='UserAgent', max_length=255, blank=True, null=True)  # Field name made lowercase.
    contextkey = models.CharField(db_column='ContextKey', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Feedback'


class Feedbacklist(models.Model):
    listid = models.AutoField(db_column='ListID', primary_key=True)  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalID')  # Field name made lowercase.
    listtype = models.IntegerField(db_column='ListType', blank=True, null=True)  # Field name made lowercase.
    isactive = models.NullBooleanField(db_column='IsActive')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    listvalue = models.CharField(db_column='ListValue', max_length=100, blank=True, null=True)  # Field name made lowercase.
    sortorder = models.IntegerField(db_column='SortOrder', blank=True, null=True)  # Field name made lowercase.
    portal = models.BooleanField(db_column='Portal')  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FeedbackList'


class Filestatistics(models.Model):
    statid = models.AutoField(db_column='StatId', primary_key=True)  # Field name made lowercase.
    fileid = models.ForeignKey('Files', models.DO_NOTHING, db_column='FileId')  # Field name made lowercase.
    statdate = models.DateTimeField(db_column='StatDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FileStatistics'


class Fileversions(models.Model):
    fileid = models.OneToOneField('Files', models.DO_NOTHING, db_column='FileId', primary_key=True)  # Field name made lowercase.
    version = models.IntegerField(db_column='Version')  # Field name made lowercase.
    filename = models.CharField(db_column='FileName', max_length=246)  # Field name made lowercase.
    extension = models.CharField(db_column='Extension', max_length=100)  # Field name made lowercase.
    size = models.IntegerField(db_column='Size')  # Field name made lowercase.
    width = models.IntegerField(db_column='Width', blank=True, null=True)  # Field name made lowercase.
    height = models.IntegerField(db_column='Height', blank=True, null=True)  # Field name made lowercase.
    contenttype = models.CharField(db_column='ContentType', max_length=200)  # Field name made lowercase.
    content = models.BinaryField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.
    sha1hash = models.CharField(db_column='SHA1Hash', max_length=40, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FileVersions'
        unique_together = (('fileid', 'version'),)


class Files(models.Model):
    fileid = models.AutoField(db_column='FileId', primary_key=True)  # Field name made lowercase.
    portalid = models.ForeignKey('Portals', models.DO_NOTHING, db_column='PortalId', blank=True, null=True)  # Field name made lowercase.
    filename = models.CharField(db_column='FileName', max_length=246)  # Field name made lowercase.
    extension = models.CharField(db_column='Extension', max_length=100)  # Field name made lowercase.
    size = models.IntegerField(db_column='Size')  # Field name made lowercase.
    width = models.IntegerField(db_column='Width', blank=True, null=True)  # Field name made lowercase.
    height = models.IntegerField(db_column='Height', blank=True, null=True)  # Field name made lowercase.
    contenttype = models.CharField(db_column='ContentType', max_length=200)  # Field name made lowercase.
    folderid = models.ForeignKey('Folders', models.DO_NOTHING, db_column='FolderID')  # Field name made lowercase.
    content = models.BinaryField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.
    uniqueid = models.CharField(db_column='UniqueId', unique=True, max_length=36)  # Field name made lowercase.
    versionguid = models.CharField(db_column='VersionGuid', max_length=36)  # Field name made lowercase.
    sha1hash = models.CharField(db_column='SHA1Hash', max_length=40, blank=True, null=True)  # Field name made lowercase.
    lastmodificationtime = models.DateTimeField(db_column='LastModificationTime')  # Field name made lowercase.
    folder = models.CharField(db_column='Folder', max_length=246, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=256, blank=True, null=True)  # Field name made lowercase.
    startdate = models.CharField(db_column='StartDate', max_length=10)  # Field name made lowercase.
    enablepublishperiod = models.BooleanField(db_column='EnablePublishPeriod')  # Field name made lowercase.
    enddate = models.CharField(db_column='EndDate', max_length=10, blank=True, null=True)  # Field name made lowercase.
    publishedversion = models.IntegerField(db_column='PublishedVersion')  # Field name made lowercase.
    contentitemid = models.ForeignKey(Contentitems, models.DO_NOTHING, db_column='ContentItemID', blank=True, null=True)  # Field name made lowercase.
    hasbeenpublished = models.BooleanField(db_column='HasBeenPublished')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Files'
        unique_together = (('portalid', 'folderid', 'filename', 'fileid', 'publishedversion'),)


class Foldermappings(models.Model):
    foldermappingid = models.AutoField(db_column='FolderMappingID', primary_key=True)  # Field name made lowercase.
    portalid = models.ForeignKey('Portals', models.DO_NOTHING, db_column='PortalID', blank=True, null=True)  # Field name made lowercase.
    mappingname = models.CharField(db_column='MappingName', max_length=50)  # Field name made lowercase.
    folderprovidertype = models.CharField(db_column='FolderProviderType', max_length=50)  # Field name made lowercase.
    priority = models.IntegerField(db_column='Priority', blank=True, null=True)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FolderMappings'
        unique_together = (('portalid', 'mappingname'),)


class Foldermappingssettings(models.Model):
    foldermappingid = models.OneToOneField(Foldermappings, models.DO_NOTHING, db_column='FolderMappingID', primary_key=True)  # Field name made lowercase.
    settingname = models.CharField(db_column='SettingName', max_length=50)  # Field name made lowercase.
    settingvalue = models.CharField(db_column='SettingValue', max_length=2000)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FolderMappingsSettings'
        unique_together = (('foldermappingid', 'settingname'),)


class Folderpermission(models.Model):
    folderpermissionid = models.AutoField(db_column='FolderPermissionID', primary_key=True)  # Field name made lowercase.
    folderid = models.ForeignKey('Folders', models.DO_NOTHING, db_column='FolderID')  # Field name made lowercase.
    permissionid = models.ForeignKey('Permission', models.DO_NOTHING, db_column='PermissionID')  # Field name made lowercase.
    allowaccess = models.BooleanField(db_column='AllowAccess')  # Field name made lowercase.
    roleid = models.ForeignKey('Roles', models.DO_NOTHING, db_column='RoleID', blank=True, null=True)  # Field name made lowercase.
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='UserID', blank=True, null=True)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FolderPermission'
        unique_together = (('roleid', 'folderid', 'permissionid', 'allowaccess'), ('userid', 'folderid', 'permissionid', 'allowaccess'), ('folderid', 'permissionid', 'roleid', 'userid', 'allowaccess'),)


class Folders(models.Model):
    folderid = models.AutoField(db_column='FolderID', primary_key=True)  # Field name made lowercase.
    portalid = models.ForeignKey('Portals', models.DO_NOTHING, db_column='PortalID', blank=True, null=True)  # Field name made lowercase.
    folderpath = models.CharField(db_column='FolderPath', max_length=300)  # Field name made lowercase.
    storagelocation = models.IntegerField(db_column='StorageLocation')  # Field name made lowercase.
    isprotected = models.BooleanField(db_column='IsProtected')  # Field name made lowercase.
    iscached = models.BooleanField(db_column='IsCached')  # Field name made lowercase.
    lastupdated = models.DateTimeField(db_column='LastUpdated', blank=True, null=True)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.
    uniqueid = models.CharField(db_column='UniqueId', unique=True, max_length=36)  # Field name made lowercase.
    versionguid = models.CharField(db_column='VersionGuid', max_length=36)  # Field name made lowercase.
    foldermappingid = models.ForeignKey(Foldermappings, models.DO_NOTHING, db_column='FolderMappingID')  # Field name made lowercase.
    parentid = models.IntegerField(db_column='ParentID', blank=True, null=True)  # Field name made lowercase.
    isversioned = models.BooleanField(db_column='IsVersioned')  # Field name made lowercase.
    workflowid = models.ForeignKey(Contentworkflows, models.DO_NOTHING, db_column='WorkflowID', blank=True, null=True)  # Field name made lowercase.
    mappedpath = models.CharField(db_column='MappedPath', max_length=300, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Folders'
        unique_together = (('portalid', 'folderpath'), ('folderid', 'portalid', 'folderpath', 'storagelocation', 'iscached', 'foldermappingid'),)


class Hostsettings(models.Model):
    settingname = models.CharField(db_column='SettingName', primary_key=True, max_length=50)  # Field name made lowercase.
    settingvalue = models.CharField(db_column='SettingValue', max_length=256)  # Field name made lowercase.
    settingissecure = models.BooleanField(db_column='SettingIsSecure')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HostSettings'


class Htmltext(models.Model):
    moduleid = models.ForeignKey('Modules', models.DO_NOTHING, db_column='ModuleID')  # Field name made lowercase.
    itemid = models.AutoField(db_column='ItemID', primary_key=True)  # Field name made lowercase.
    content = models.TextField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    version = models.IntegerField(db_column='Version', blank=True, null=True)  # Field name made lowercase.
    stateid = models.IntegerField(db_column='StateID', blank=True, null=True)  # Field name made lowercase.
    ispublished = models.NullBooleanField(db_column='IsPublished')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.
    summary = models.TextField(db_column='Summary', blank=True, null=True)  # Field name made lowercase.
    publishdate = models.DateTimeField(db_column='PublishDate', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return str(self.itemid)

    class Meta:
        managed = False
        db_table = 'HtmlText'


class Htmltextlog(models.Model):
    htmltextlogid = models.AutoField(db_column='HtmlTextLogID', primary_key=True)  # Field name made lowercase.
    itemid = models.ForeignKey(Htmltext, models.DO_NOTHING, db_column='ItemID')  # Field name made lowercase.
    stateid = models.IntegerField(db_column='StateID')  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    approved = models.BooleanField(db_column='Approved')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID')  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HtmlTextLog'


class Ipfilter(models.Model):
    ipfilterid = models.AutoField(db_column='IPFilterID', primary_key=True)  # Field name made lowercase.
    ipaddress = models.CharField(db_column='IPAddress', max_length=50, blank=True, null=True)  # Field name made lowercase.
    subnetmask = models.CharField(db_column='SubnetMask', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ruletype = models.SmallIntegerField(db_column='RuleType', blank=True, null=True)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'IPFilter'


class Javascriptlibraries(models.Model):
    javascriptlibraryid = models.AutoField(db_column='JavaScriptLibraryID', primary_key=True)  # Field name made lowercase.
    packageid = models.ForeignKey('Packages', models.DO_NOTHING, db_column='PackageID')  # Field name made lowercase.
    libraryname = models.CharField(db_column='LibraryName', max_length=200)  # Field name made lowercase.
    version = models.CharField(db_column='Version', max_length=50)  # Field name made lowercase.
    filename = models.CharField(db_column='FileName', max_length=100)  # Field name made lowercase.
    objectname = models.CharField(db_column='ObjectName', max_length=100)  # Field name made lowercase.
    preferredscriptlocation = models.IntegerField(db_column='PreferredScriptLocation')  # Field name made lowercase.
    cdnpath = models.CharField(db_column='CDNPath', max_length=250)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'JavaScriptLibraries'


class Journal(models.Model):
    journalid = models.AutoField(db_column='JournalId', primary_key=True)  # Field name made lowercase.
    journaltypeid = models.ForeignKey('JournalTypes', models.DO_NOTHING, db_column='JournalTypeId')  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserId', blank=True, null=True)  # Field name made lowercase.
    datecreated = models.DateTimeField(db_column='DateCreated', blank=True, null=True)  # Field name made lowercase.
    dateupdated = models.DateTimeField(db_column='DateUpdated', blank=True, null=True)  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId', blank=True, null=True)  # Field name made lowercase.
    profileid = models.IntegerField(db_column='ProfileId')  # Field name made lowercase.
    groupid = models.IntegerField(db_column='GroupId')  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=255, blank=True, null=True)  # Field name made lowercase.
    summary = models.CharField(db_column='Summary', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    itemdata = models.CharField(db_column='ItemData', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    imageurl = models.CharField(db_column='ImageURL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objectkey = models.CharField(db_column='ObjectKey', max_length=255, blank=True, null=True)  # Field name made lowercase.
    accesskey = models.CharField(db_column='AccessKey', max_length=36, blank=True, null=True)  # Field name made lowercase.
    contentitemid = models.IntegerField(db_column='ContentItemId', blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.BooleanField(db_column='IsDeleted')  # Field name made lowercase.
    commentsdisabled = models.BooleanField(db_column='CommentsDisabled')  # Field name made lowercase.
    commentshidden = models.BooleanField(db_column='CommentsHidden')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Journal'


class JournalAccess(models.Model):
    journalaccessid = models.AutoField(db_column='JournalAccessId', primary_key=True)  # Field name made lowercase.
    journaltypeid = models.IntegerField(db_column='JournalTypeId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50)  # Field name made lowercase.
    accesskey = models.CharField(db_column='AccessKey', max_length=36)  # Field name made lowercase.
    isenabled = models.BooleanField(db_column='IsEnabled')  # Field name made lowercase.
    datecreated = models.DateTimeField(db_column='DateCreated')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Journal_Access'


class JournalComments(models.Model):
    commentid = models.AutoField(db_column='CommentId', primary_key=True)  # Field name made lowercase.
    journalid = models.ForeignKey(Journal, models.DO_NOTHING, db_column='JournalId')  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserId')  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    datecreated = models.DateTimeField(db_column='DateCreated')  # Field name made lowercase.
    dateupdated = models.DateTimeField(db_column='DateUpdated')  # Field name made lowercase.
    commentxml = models.TextField(db_column='CommentXML', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Journal_Comments'


class JournalData(models.Model):
    journaldataid = models.AutoField(db_column='JournalDataId', primary_key=True)  # Field name made lowercase.
    journalid = models.ForeignKey(Journal, models.DO_NOTHING, db_column='JournalId')  # Field name made lowercase.
    journalxml = models.TextField(db_column='JournalXML')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Journal_Data'


class JournalSecurity(models.Model):
    journalsecurityid = models.AutoField(db_column='JournalSecurityId', primary_key=True)  # Field name made lowercase.
    journalid = models.IntegerField(db_column='JournalId')  # Field name made lowercase.
    securitykey = models.CharField(db_column='SecurityKey', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Journal_Security'
        unique_together = (('journalid', 'securitykey'),)


class JournalTypefilters(models.Model):
    journaltypefilterid = models.AutoField(db_column='JournalTypeFilterId', primary_key=True)  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    journaltypeid = models.IntegerField(db_column='JournalTypeId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Journal_TypeFilters'


class JournalTypes(models.Model):
    journaltypeid = models.IntegerField(db_column='JournalTypeId', primary_key=True)  # Field name made lowercase.
    journaltype = models.CharField(db_column='JournalType', max_length=25, blank=True, null=True)  # Field name made lowercase.
    icon = models.CharField(max_length=25, blank=True, null=True)
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    isenabled = models.BooleanField(db_column='IsEnabled')  # Field name made lowercase.
    appliestoprofile = models.BooleanField(db_column='AppliesToProfile')  # Field name made lowercase.
    appliestogroup = models.BooleanField(db_column='AppliesToGroup')  # Field name made lowercase.
    appliestostream = models.BooleanField(db_column='AppliesToStream')  # Field name made lowercase.
    options = models.TextField(db_column='Options', blank=True, null=True)  # Field name made lowercase.
    supportsnotify = models.BooleanField(db_column='SupportsNotify')  # Field name made lowercase.
    enablecomments = models.BooleanField(db_column='EnableComments')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Journal_Types'


class Languagepacks(models.Model):
    languagepackid = models.AutoField(db_column='LanguagePackID', primary_key=True)  # Field name made lowercase.
    packageid = models.ForeignKey('Packages', models.DO_NOTHING, db_column='PackageID')  # Field name made lowercase.
    dependentpackageid = models.IntegerField(db_column='DependentPackageID')  # Field name made lowercase.
    languageid = models.IntegerField(db_column='LanguageID')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LanguagePacks'
        unique_together = (('languageid', 'packageid'),)


class Languages(models.Model):
    languageid = models.AutoField(db_column='LanguageID', primary_key=True)  # Field name made lowercase.
    culturecode = models.CharField(db_column='CultureCode', unique=True, max_length=50)  # Field name made lowercase.
    culturename = models.CharField(db_column='CultureName', max_length=200)  # Field name made lowercase.
    fallbackculture = models.CharField(db_column='FallbackCulture', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Languages'


class Lists(models.Model):
    entryid = models.AutoField(db_column='EntryID', primary_key=True)  # Field name made lowercase.
    listname = models.CharField(db_column='ListName', max_length=50)  # Field name made lowercase.
    value = models.CharField(db_column='Value', max_length=100)  # Field name made lowercase.
    text = models.CharField(db_column='Text', max_length=150)  # Field name made lowercase.
    parentid = models.IntegerField(db_column='ParentID')  # Field name made lowercase.
    level = models.IntegerField(db_column='Level')  # Field name made lowercase.
    sortorder = models.IntegerField(db_column='SortOrder')  # Field name made lowercase.
    definitionid = models.IntegerField(db_column='DefinitionID')  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=500, blank=True, null=True)  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalID')  # Field name made lowercase.
    systemlist = models.BooleanField(db_column='SystemList')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Lists'
        unique_together = (('listname', 'value', 'text', 'parentid'), ('parentid', 'listname', 'value', 'sortorder', 'definitionid', 'text'),)


class MechanicsBadge(models.Model):
    badgeid = models.AutoField(db_column='BadgeId', primary_key=True)  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    badgename = models.CharField(db_column='BadgeName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    tier = models.IntegerField(db_column='Tier')  # Field name made lowercase.
    timeframeindays = models.IntegerField(db_column='TimeFrameInDays')  # Field name made lowercase.
    imagefileid = models.IntegerField(db_column='ImageFileId')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID')  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate')  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID')  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mechanics_Badge'


class MechanicsBadgescoactdef(models.Model):
    badgesadid = models.AutoField(db_column='BadgeSadId', primary_key=True)  # Field name made lowercase.
    badgeid = models.ForeignKey(MechanicsBadge, models.DO_NOTHING, db_column='BadgeId')  # Field name made lowercase.
    scoringactiondefid = models.ForeignKey('MechanicsScoringactiondefinition', models.DO_NOTHING, db_column='ScoringActionDefId')  # Field name made lowercase.
    numberoftimes = models.IntegerField(db_column='NumberOfTimes')  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mechanics_BadgeScoActDef'


class MechanicsPrivilege(models.Model):
    privilegeid = models.AutoField(db_column='PrivilegeId', primary_key=True)  # Field name made lowercase.
    privilegedefid = models.ForeignKey('MechanicsPrivilegedefinition', models.DO_NOTHING, db_column='PrivilegeDefId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    reputationpoints = models.IntegerField(db_column='ReputationPoints')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID')  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate')  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID')  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mechanics_Privilege'
        unique_together = (('privilegedefid', 'portalid'),)


class MechanicsPrivilegedefinition(models.Model):
    privilegedefid = models.AutoField(db_column='PrivilegeDefId', primary_key=True)  # Field name made lowercase.
    privilegename = models.CharField(db_column='PrivilegeName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    defaultreputationpoints = models.IntegerField(db_column='DefaultReputationPoints')  # Field name made lowercase.
    desktopmoduleid = models.IntegerField(db_column='DesktopModuleId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mechanics_PrivilegeDefinition'


class MechanicsScoringaction(models.Model):
    scoringactionid = models.AutoField(db_column='ScoringActionId', primary_key=True)  # Field name made lowercase.
    scoringactiondefid = models.ForeignKey('MechanicsScoringactiondefinition', models.DO_NOTHING, db_column='ScoringActionDefId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    experiencepoints = models.IntegerField(db_column='ExperiencePoints')  # Field name made lowercase.
    reputationpoints = models.IntegerField(db_column='ReputationPoints')  # Field name made lowercase.
    maxcount = models.IntegerField(db_column='MaxCount')  # Field name made lowercase.
    interval = models.IntegerField(db_column='Interval')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID')  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate')  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID')  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mechanics_ScoringAction'


class MechanicsScoringactiondefinition(models.Model):
    scoringactiondefid = models.AutoField(db_column='ScoringActionDefId', primary_key=True)  # Field name made lowercase.
    actionname = models.CharField(db_column='ActionName', max_length=100)  # Field name made lowercase.
    defaultexperiencepoints = models.IntegerField(db_column='DefaultExperiencePoints')  # Field name made lowercase.
    defaultreputationpoints = models.IntegerField(db_column='DefaultReputationPoints')  # Field name made lowercase.
    defaultmaxcount = models.IntegerField(db_column='DefaultMaxCount')  # Field name made lowercase.
    defaultinterval = models.IntegerField(db_column='DefaultInterval')  # Field name made lowercase.
    desktopmoduleid = models.IntegerField(db_column='DesktopModuleId')  # Field name made lowercase.
    actiontype = models.IntegerField(db_column='ActionType')  # Field name made lowercase.
    packageid = models.IntegerField(db_column='PackageId')  # Field name made lowercase.
    isenabled = models.BooleanField(db_column='IsEnabled')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mechanics_ScoringActionDefinition'


class MechanicsUserbadge(models.Model):
    userbadgeid = models.AutoField(db_column='UserBadgeId', primary_key=True)  # Field name made lowercase.
    badgeid = models.ForeignKey(MechanicsBadge, models.DO_NOTHING, db_column='BadgeId')  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mechanics_UserBadge'


class MechanicsUserscoring(models.Model):
    userscoringid = models.AutoField(db_column='UserScoringId', primary_key=True)  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    experiencepoints = models.IntegerField(db_column='ExperiencePoints')  # Field name made lowercase.
    reputationpoints = models.IntegerField(db_column='ReputationPoints')  # Field name made lowercase.
    topreputationpoints = models.IntegerField(db_column='TopReputationPoints')  # Field name made lowercase.
    dailyreputationpoints = models.IntegerField(db_column='DailyReputationPoints')  # Field name made lowercase.
    bestreputationpoints = models.IntegerField(db_column='BestReputationPoints')  # Field name made lowercase.
    contentviewedcount = models.IntegerField(db_column='ContentViewedCount')  # Field name made lowercase.
    contentinteractedcount = models.IntegerField(db_column='ContentInteractedCount')  # Field name made lowercase.
    contentcreatedcount = models.IntegerField(db_column='ContentCreatedCount')  # Field name made lowercase.
    contenteditedcount = models.IntegerField(db_column='ContentEditedCount')  # Field name made lowercase.
    contentdeletedcount = models.IntegerField(db_column='ContentDeletedCount')  # Field name made lowercase.
    contentflaggedcount = models.IntegerField(db_column='ContentFlaggedCount')  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate')  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mechanics_UserScoring'


class MechanicsUserscoringlog(models.Model):
    userscoringlogid = models.AutoField(db_column='UserScoringLogId', primary_key=True)  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserId')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    contentitemid = models.IntegerField(db_column='ContentItemId', blank=True, null=True)  # Field name made lowercase.
    notes = models.CharField(db_column='Notes', max_length=400, blank=True, null=True)  # Field name made lowercase.
    context = models.CharField(db_column='Context', max_length=1500, blank=True, null=True)  # Field name made lowercase.
    scoringactiondefid = models.ForeignKey(MechanicsScoringactiondefinition, models.DO_NOTHING, db_column='ScoringActionDefId')  # Field name made lowercase.
    experiencepoints = models.IntegerField(db_column='ExperiencePoints')  # Field name made lowercase.
    reputationpoints = models.IntegerField(db_column='ReputationPoints')  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate')  # Field name made lowercase.
    groupid = models.DecimalField(db_column='GroupId', max_digits=18, decimal_places=0)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mechanics_UserScoringLog'


class MechanicsVisitorscoring(models.Model):
    visitorscoringid = models.AutoField(db_column='VisitorScoringId', primary_key=True)  # Field name made lowercase.
    visitorid = models.CharField(db_column='VisitorId', max_length=36)  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    experiencepoints = models.IntegerField(db_column='ExperiencePoints')  # Field name made lowercase.
    reputationpoints = models.IntegerField(db_column='ReputationPoints')  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate')  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mechanics_VisitorScoring'


class MechanicsVisitorscoringlog(models.Model):
    visitorscoringlogid = models.AutoField(db_column='VisitorScoringLogId', primary_key=True)  # Field name made lowercase.
    visitorid = models.CharField(db_column='VisitorId', max_length=36)  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    contentitemid = models.IntegerField(db_column='ContentItemId', blank=True, null=True)  # Field name made lowercase.
    context = models.CharField(db_column='Context', max_length=1500, blank=True, null=True)  # Field name made lowercase.
    scoringactiondefid = models.ForeignKey(MechanicsScoringactiondefinition, models.DO_NOTHING, db_column='ScoringActionDefId')  # Field name made lowercase.
    experiencepoints = models.IntegerField(db_column='ExperiencePoints')  # Field name made lowercase.
    reputationpoints = models.IntegerField(db_column='ReputationPoints')  # Field name made lowercase.
    groupid = models.IntegerField(db_column='GroupId')  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mechanics_VisitorScoringLog'


class MessagingMessages(models.Model):
    messageid = models.BigAutoField(db_column='MessageID', primary_key=True)  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalID')  # Field name made lowercase.
    fromuserid = models.IntegerField(db_column='FromUserID')  # Field name made lowercase.
    tousername = models.CharField(db_column='ToUserName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fromusername = models.CharField(db_column='FromUserName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    touserid = models.IntegerField(db_column='ToUserID', blank=True, null=True)  # Field name made lowercase.
    toroleid = models.IntegerField(db_column='ToRoleID', blank=True, null=True)  # Field name made lowercase.
    status = models.SmallIntegerField(db_column='Status')  # Field name made lowercase.
    subject = models.TextField(db_column='Subject', blank=True, null=True)  # Field name made lowercase.
    body = models.TextField(db_column='Body', blank=True, null=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date')  # Field name made lowercase.
    conversation = models.CharField(db_column='Conversation', max_length=36)  # Field name made lowercase.
    replyto = models.BigIntegerField(db_column='ReplyTo', blank=True, null=True)  # Field name made lowercase.
    allowreply = models.BooleanField(db_column='AllowReply')  # Field name made lowercase.
    skipportal = models.BooleanField(db_column='SkipPortal')  # Field name made lowercase.
    emailsent = models.BooleanField(db_column='EmailSent')  # Field name made lowercase.
    emailsentdate = models.DateTimeField(db_column='EmailSentDate', blank=True, null=True)  # Field name made lowercase.
    emailschedulerinstance = models.CharField(db_column='EmailSchedulerInstance', max_length=36, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Messaging_Messages'


class Metadata(models.Model):
    metadataid = models.AutoField(db_column='MetaDataID', primary_key=True)  # Field name made lowercase.
    metadataname = models.CharField(db_column='MetaDataName', unique=True, max_length=100)  # Field name made lowercase.
    metadatadescription = models.CharField(db_column='MetaDataDescription', max_length=2500, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MetaData'


class MobilePreviewprofiles(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    portalid = models.ForeignKey('Portals', models.DO_NOTHING, db_column='PortalId')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50)  # Field name made lowercase.
    width = models.IntegerField(db_column='Width')  # Field name made lowercase.
    height = models.IntegerField(db_column='Height')  # Field name made lowercase.
    useragent = models.CharField(db_column='UserAgent', max_length=260)  # Field name made lowercase.
    sortorder = models.IntegerField(db_column='SortOrder')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID')  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate')  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID')  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mobile_PreviewProfiles'


class MobileRedirectionrules(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    redirectionid = models.ForeignKey('MobileRedirections', models.DO_NOTHING, db_column='RedirectionId')  # Field name made lowercase.
    capability = models.CharField(db_column='Capability', max_length=50)  # Field name made lowercase.
    expression = models.CharField(db_column='Expression', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mobile_RedirectionRules'


class MobileRedirections(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    portalid = models.ForeignKey('Portals', models.DO_NOTHING, db_column='PortalId')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50)  # Field name made lowercase.
    type = models.IntegerField(db_column='Type')  # Field name made lowercase.
    sortorder = models.IntegerField(db_column='SortOrder')  # Field name made lowercase.
    sourcetabid = models.IntegerField(db_column='SourceTabId')  # Field name made lowercase.
    includechildtabs = models.BooleanField(db_column='IncludeChildTabs')  # Field name made lowercase.
    targettype = models.IntegerField(db_column='TargetType')  # Field name made lowercase.
    targetvalue = models.CharField(db_column='TargetValue', max_length=260)  # Field name made lowercase.
    enabled = models.BooleanField(db_column='Enabled')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID')  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate')  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID')  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mobile_Redirections'


class Modulecache(models.Model):
    cachekey = models.CharField(db_column='CacheKey', primary_key=True, max_length=36)  # Field name made lowercase.
    itemid = models.IntegerField(db_column='ItemId')  # Field name made lowercase.
    data = models.TextField(db_column='Data')  # Field name made lowercase.
    expiration = models.DateTimeField(db_column='Expiration')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ModuleCache'


class Modulecontrols(models.Model):
    modulecontrolid = models.AutoField(db_column='ModuleControlID', primary_key=True)  # Field name made lowercase.
    moduledefid = models.ForeignKey('Moduledefinitions', models.DO_NOTHING, db_column='ModuleDefID', blank=True, null=True)  # Field name made lowercase.
    controlkey = models.CharField(db_column='ControlKey', max_length=50, blank=True, null=True)  # Field name made lowercase.
    controltitle = models.CharField(db_column='ControlTitle', max_length=50, blank=True, null=True)  # Field name made lowercase.
    controlsrc = models.CharField(db_column='ControlSrc', max_length=256, blank=True, null=True)  # Field name made lowercase.
    iconfile = models.CharField(db_column='IconFile', max_length=100, blank=True, null=True)  # Field name made lowercase.
    controltype = models.IntegerField(db_column='ControlType')  # Field name made lowercase.
    vieworder = models.IntegerField(db_column='ViewOrder', blank=True, null=True)  # Field name made lowercase.
    helpurl = models.CharField(db_column='HelpUrl', max_length=200, blank=True, null=True)  # Field name made lowercase.
    supportspartialrendering = models.BooleanField(db_column='SupportsPartialRendering')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.
    supportspopups = models.BooleanField(db_column='SupportsPopUps')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ModuleControls'
        unique_together = (('moduledefid', 'controlkey', 'controlsrc'),)


class Moduledefinitions(models.Model):
    moduledefid = models.AutoField(db_column='ModuleDefID', primary_key=True)  # Field name made lowercase.
    friendlyname = models.CharField(db_column='FriendlyName', max_length=128)  # Field name made lowercase.
    desktopmoduleid = models.ForeignKey(Desktopmodules, models.DO_NOTHING, db_column='DesktopModuleID')  # Field name made lowercase.
    defaultcachetime = models.IntegerField(db_column='DefaultCacheTime')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.
    definitionname = models.CharField(db_column='DefinitionName', unique=True, max_length=128)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ModuleDefinitions'


class Modulepermission(models.Model):
    modulepermissionid = models.AutoField(db_column='ModulePermissionID', primary_key=True)  # Field name made lowercase.
    moduleid = models.ForeignKey('Modules', models.DO_NOTHING, db_column='ModuleID')  # Field name made lowercase.
    permissionid = models.ForeignKey('Permission', models.DO_NOTHING, db_column='PermissionID')  # Field name made lowercase.
    allowaccess = models.BooleanField(db_column='AllowAccess')  # Field name made lowercase.
    roleid = models.ForeignKey('Roles', models.DO_NOTHING, db_column='RoleID', blank=True, null=True)  # Field name made lowercase.
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='UserID', blank=True, null=True)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ModulePermission'
        unique_together = (('moduleid', 'permissionid', 'portalid', 'roleid', 'userid', 'allowaccess'), ('userid', 'moduleid', 'permissionid', 'portalid', 'allowaccess'), ('roleid', 'moduleid', 'permissionid', 'portalid', 'allowaccess'),)


class Modulesettings(models.Model):
    moduleid = models.OneToOneField('Modules', models.DO_NOTHING, db_column='ModuleID', primary_key=True)  # Field name made lowercase.
    settingname = models.CharField(db_column='SettingName', max_length=50)  # Field name made lowercase.
    settingvalue = models.TextField(db_column='SettingValue')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ModuleSettings'
        unique_together = (('moduleid', 'settingname'),)


class Modules(models.Model):
    moduleid = models.AutoField(db_column='ModuleID', primary_key=True)  # Field name made lowercase.
    moduledefid = models.ForeignKey(Moduledefinitions, models.DO_NOTHING, db_column='ModuleDefID')  # Field name made lowercase.
    alltabs = models.BooleanField(db_column='AllTabs')  # Field name made lowercase.
    isdeleted = models.BooleanField(db_column='IsDeleted')  # Field name made lowercase.
    inheritviewpermissions = models.NullBooleanField(db_column='InheritViewPermissions')  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalID', blank=True, null=True)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastcontentmodifiedondate = models.DateTimeField(db_column='LastContentModifiedOnDate', blank=True, null=True)  # Field name made lowercase.
    contentitemid = models.ForeignKey(Contentitems, models.DO_NOTHING, db_column='ContentItemID', blank=True, null=True)  # Field name made lowercase.
    isshareable = models.BooleanField(db_column='IsShareable')  # Field name made lowercase.
    isshareableviewonly = models.BooleanField(db_column='IsShareableViewOnly')  # Field name made lowercase.

    def __str__(self):
        return str(self.moduleid)

    class Meta:
        managed = False
        db_table = 'Modules'


class Outputcache(models.Model):
    cachekey = models.CharField(db_column='CacheKey', primary_key=True, max_length=36)  # Field name made lowercase.
    itemid = models.IntegerField(db_column='ItemId')  # Field name made lowercase.
    data = models.TextField(db_column='Data')  # Field name made lowercase.
    expiration = models.DateTimeField(db_column='Expiration')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OutputCache'


class Packagedependencies(models.Model):
    packagedependencyid = models.AutoField(db_column='PackageDependencyID', primary_key=True)  # Field name made lowercase.
    packageid = models.ForeignKey('Packages', models.DO_NOTHING, db_column='PackageID')  # Field name made lowercase.
    packagename = models.CharField(db_column='PackageName', max_length=128)  # Field name made lowercase.
    version = models.CharField(db_column='Version', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PackageDependencies'


class Packagetypes(models.Model):
    packagetype = models.CharField(db_column='PackageType', primary_key=True, max_length=100)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=500)  # Field name made lowercase.
    securityaccesslevel = models.IntegerField(db_column='SecurityAccessLevel')  # Field name made lowercase.
    editorcontrolsrc = models.CharField(db_column='EditorControlSrc', max_length=250, blank=True, null=True)  # Field name made lowercase.
    supportssidebysideinstallation = models.BooleanField(db_column='SupportsSideBySideInstallation')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PackageTypes'


class Packages(models.Model):
    packageid = models.AutoField(db_column='PackageID', primary_key=True)  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalID', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=128)  # Field name made lowercase.
    friendlyname = models.CharField(db_column='FriendlyName', max_length=250)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    packagetype = models.ForeignKey(Packagetypes, models.DO_NOTHING, db_column='PackageType')  # Field name made lowercase.
    version = models.CharField(db_column='Version', max_length=50)  # Field name made lowercase.
    license = models.TextField(db_column='License', blank=True, null=True)  # Field name made lowercase.
    manifest = models.TextField(db_column='Manifest', blank=True, null=True)  # Field name made lowercase.
    owner = models.CharField(db_column='Owner', max_length=100, blank=True, null=True)  # Field name made lowercase.
    organization = models.CharField(db_column='Organization', max_length=100, blank=True, null=True)  # Field name made lowercase.
    url = models.CharField(db_column='Url', max_length=250, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)  # Field name made lowercase.
    releasenotes = models.TextField(db_column='ReleaseNotes', blank=True, null=True)  # Field name made lowercase.
    issystempackage = models.BooleanField(db_column='IsSystemPackage')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.
    foldername = models.CharField(db_column='FolderName', max_length=128, blank=True, null=True)  # Field name made lowercase.
    iconfile = models.CharField(db_column='IconFile', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Packages'
        unique_together = (('owner', 'name', 'packagetype', 'portalid', 'version'),)


class Passwordhistory(models.Model):
    passwordhistoryid = models.AutoField(db_column='PasswordHistoryID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='UserID')  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=128)  # Field name made lowercase.
    passwordsalt = models.CharField(db_column='PasswordSalt', max_length=128)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PasswordHistory'


class Permission(models.Model):
    permissionid = models.AutoField(db_column='PermissionID', primary_key=True)  # Field name made lowercase.
    permissioncode = models.CharField(db_column='PermissionCode', max_length=50)  # Field name made lowercase.
    moduledefid = models.IntegerField(db_column='ModuleDefID')  # Field name made lowercase.
    permissionkey = models.CharField(db_column='PermissionKey', max_length=50)  # Field name made lowercase.
    permissionname = models.CharField(db_column='PermissionName', max_length=50)  # Field name made lowercase.
    vieworder = models.IntegerField(db_column='ViewOrder')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Permission'
        unique_together = (('permissioncode', 'moduledefid', 'permissionkey'),)


class Portalalias(models.Model):
    portalaliasid = models.AutoField(db_column='PortalAliasID', primary_key=True)  # Field name made lowercase.
    portalid = models.ForeignKey('Portals', models.DO_NOTHING, db_column='PortalID')  # Field name made lowercase.
    httpalias = models.CharField(db_column='HTTPAlias', unique=True, max_length=200, blank=True, null=True)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.
    browsertype = models.CharField(db_column='BrowserType', max_length=10, blank=True, null=True)  # Field name made lowercase.
    skin = models.CharField(db_column='Skin', max_length=100, blank=True, null=True)  # Field name made lowercase.
    culturecode = models.CharField(db_column='CultureCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    isprimary = models.BooleanField(db_column='IsPrimary')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PortalAlias'


class Portaldesktopmodules(models.Model):
    portaldesktopmoduleid = models.AutoField(db_column='PortalDesktopModuleID', primary_key=True)  # Field name made lowercase.
    portalid = models.ForeignKey('Portals', models.DO_NOTHING, db_column='PortalID')  # Field name made lowercase.
    desktopmoduleid = models.ForeignKey(Desktopmodules, models.DO_NOTHING, db_column='DesktopModuleID')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PortalDesktopModules'
        unique_together = (('portalid', 'desktopmoduleid'),)


class Portalgroups(models.Model):
    portalgroupid = models.AutoField(db_column='PortalGroupID', primary_key=True)  # Field name made lowercase.
    masterportalid = models.IntegerField(db_column='MasterPortalID', blank=True, null=True)  # Field name made lowercase.
    portalgroupname = models.CharField(db_column='PortalGroupName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    portalgroupdescription = models.CharField(db_column='PortalGroupDescription', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    authenticationdomain = models.CharField(db_column='AuthenticationDomain', max_length=200, blank=True, null=True)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PortalGroups'


class Portallanguages(models.Model):
    portallanguageid = models.AutoField(db_column='PortalLanguageID', primary_key=True)  # Field name made lowercase.
    portalid = models.ForeignKey('Portals', models.DO_NOTHING, db_column='PortalID')  # Field name made lowercase.
    languageid = models.ForeignKey(Languages, models.DO_NOTHING, db_column='LanguageID')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.
    ispublished = models.BooleanField(db_column='IsPublished')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PortalLanguages'
        unique_together = (('portalid', 'languageid'),)


class Portallocalization(models.Model):
    portalid = models.OneToOneField('Portals', models.DO_NOTHING, db_column='PortalID', primary_key=True)  # Field name made lowercase.
    culturecode = models.CharField(db_column='CultureCode', max_length=10)  # Field name made lowercase.
    portalname = models.CharField(db_column='PortalName', max_length=128)  # Field name made lowercase.
    logofile = models.CharField(db_column='LogoFile', max_length=50, blank=True, null=True)  # Field name made lowercase.
    footertext = models.CharField(db_column='FooterText', max_length=100, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=500, blank=True, null=True)  # Field name made lowercase.
    keywords = models.CharField(db_column='KeyWords', max_length=500, blank=True, null=True)  # Field name made lowercase.
    backgroundfile = models.CharField(db_column='BackgroundFile', max_length=50, blank=True, null=True)  # Field name made lowercase.
    hometabid = models.IntegerField(db_column='HomeTabId', blank=True, null=True)  # Field name made lowercase.
    logintabid = models.IntegerField(db_column='LoginTabId', blank=True, null=True)  # Field name made lowercase.
    usertabid = models.IntegerField(db_column='UserTabId', blank=True, null=True)  # Field name made lowercase.
    admintabid = models.IntegerField(db_column='AdminTabId', blank=True, null=True)  # Field name made lowercase.
    splashtabid = models.IntegerField(db_column='SplashTabId', blank=True, null=True)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.
    registertabid = models.IntegerField(db_column='RegisterTabId', blank=True, null=True)  # Field name made lowercase.
    searchtabid = models.IntegerField(db_column='SearchTabId', blank=True, null=True)  # Field name made lowercase.
    custom404tabid = models.IntegerField(db_column='Custom404TabId', blank=True, null=True)  # Field name made lowercase.
    custom500tabid = models.IntegerField(db_column='Custom500TabId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PortalLocalization'
        unique_together = (('portalid', 'culturecode'),)


class Portalsettings(models.Model):
    portalsettingid = models.AutoField(db_column='PortalSettingID', primary_key=True)  # Field name made lowercase.
    portalid = models.ForeignKey('Portals', models.DO_NOTHING, db_column='PortalID')  # Field name made lowercase.
    settingname = models.CharField(db_column='SettingName', max_length=50)  # Field name made lowercase.
    settingvalue = models.CharField(db_column='SettingValue', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.
    culturecode = models.CharField(db_column='CultureCode', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PortalSettings'
        unique_together = (('portalid', 'settingname', 'culturecode'),)


class Portals(models.Model):
    portalid = models.AutoField(db_column='PortalID', primary_key=True)  # Field name made lowercase.
    expirydate = models.DateTimeField(db_column='ExpiryDate', blank=True, null=True)  # Field name made lowercase.
    userregistration = models.IntegerField(db_column='UserRegistration')  # Field name made lowercase.
    banneradvertising = models.IntegerField(db_column='BannerAdvertising')  # Field name made lowercase.
    administratorid = models.IntegerField(db_column='AdministratorId', blank=True, null=True)  # Field name made lowercase.
    currency = models.CharField(db_column='Currency', max_length=3, blank=True, null=True)  # Field name made lowercase.
    hostfee = models.DecimalField(db_column='HostFee', max_digits=19, decimal_places=4)  # Field name made lowercase.
    hostspace = models.IntegerField(db_column='HostSpace')  # Field name made lowercase.
    administratorroleid = models.IntegerField(db_column='AdministratorRoleId', blank=True, null=True)  # Field name made lowercase.
    registeredroleid = models.IntegerField(db_column='RegisteredRoleId', blank=True, null=True)  # Field name made lowercase.
    guid = models.CharField(db_column='GUID', max_length=36)  # Field name made lowercase.
    paymentprocessor = models.CharField(db_column='PaymentProcessor', max_length=50, blank=True, null=True)  # Field name made lowercase.
    processoruserid = models.CharField(db_column='ProcessorUserId', max_length=50, blank=True, null=True)  # Field name made lowercase.
    processorpassword = models.CharField(db_column='ProcessorPassword', max_length=50, blank=True, null=True)  # Field name made lowercase.
    siteloghistory = models.IntegerField(db_column='SiteLogHistory', blank=True, null=True)  # Field name made lowercase.
    defaultlanguage = models.CharField(db_column='DefaultLanguage', max_length=10)  # Field name made lowercase.
    timezoneoffset = models.IntegerField(db_column='TimezoneOffset')  # Field name made lowercase.
    homedirectory = models.CharField(db_column='HomeDirectory', max_length=100)  # Field name made lowercase.
    pagequota = models.IntegerField(db_column='PageQuota')  # Field name made lowercase.
    userquota = models.IntegerField(db_column='UserQuota')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.
    portalgroupid = models.IntegerField(db_column='PortalGroupID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Portals'


class Profile(models.Model):
    profileid = models.AutoField(db_column='ProfileId', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='UserId')  # Field name made lowercase.
    portalid = models.ForeignKey(Portals, models.DO_NOTHING, db_column='PortalId')  # Field name made lowercase.
    profiledata = models.TextField(db_column='ProfileData')  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Profile'
        unique_together = (('userid', 'portalid'),)


class Profilepropertydefinition(models.Model):
    propertydefinitionid = models.AutoField(db_column='PropertyDefinitionID', primary_key=True)  # Field name made lowercase.
    portalid = models.ForeignKey(Portals, models.DO_NOTHING, db_column='PortalID', blank=True, null=True)  # Field name made lowercase.
    moduledefid = models.IntegerField(db_column='ModuleDefID', blank=True, null=True)  # Field name made lowercase.
    deleted = models.BooleanField(db_column='Deleted')  # Field name made lowercase.
    datatype = models.IntegerField(db_column='DataType')  # Field name made lowercase.
    defaultvalue = models.TextField(db_column='DefaultValue', blank=True, null=True)  # Field name made lowercase.
    propertycategory = models.CharField(db_column='PropertyCategory', max_length=50)  # Field name made lowercase.
    propertyname = models.CharField(db_column='PropertyName', max_length=50)  # Field name made lowercase.
    length = models.IntegerField(db_column='Length')  # Field name made lowercase.
    required = models.BooleanField(db_column='Required')  # Field name made lowercase.
    validationexpression = models.CharField(db_column='ValidationExpression', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    vieworder = models.IntegerField(db_column='ViewOrder')  # Field name made lowercase.
    visible = models.BooleanField(db_column='Visible')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.
    defaultvisibility = models.IntegerField(db_column='DefaultVisibility', blank=True, null=True)  # Field name made lowercase.
    readonly = models.BooleanField(db_column='ReadOnly')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ProfilePropertyDefinition'
        unique_together = (('portalid', 'moduledefid', 'propertyname'),)


class PublisherPosts(models.Model):
    postid = models.AutoField(db_column='PostId', primary_key=True)  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    groupid = models.IntegerField(db_column='GroupId', blank=True, null=True)  # Field name made lowercase.
    contentitemid = models.IntegerField(db_column='ContentItemId')  # Field name made lowercase.
    published = models.BooleanField(db_column='Published')  # Field name made lowercase.
    allowedcomments = models.BooleanField(db_column='AllowedComments')  # Field name made lowercase.
    featured = models.BooleanField(db_column='Featured')  # Field name made lowercase.
    authoruserid = models.IntegerField(db_column='AuthorUserId')  # Field name made lowercase.
    metadatatitle = models.TextField(db_column='MetadataTitle')  # Field name made lowercase.
    iscustommetadatatitle = models.BooleanField(db_column='IsCustomMetadataTitle')  # Field name made lowercase.
    metadatadescription = models.TextField(db_column='MetadataDescription')  # Field name made lowercase.
    iscustommetadatadescription = models.BooleanField(db_column='IsCustomMetadataDescription')  # Field name made lowercase.
    publishedondate = models.DateTimeField(db_column='PublishedOnDate', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate')  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Publisher_Posts'


class Relationshiptypes(models.Model):
    relationshiptypeid = models.AutoField(db_column='RelationshipTypeID', primary_key=True)  # Field name made lowercase.
    direction = models.IntegerField(db_column='Direction')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=500, blank=True, null=True)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID')  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate')  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID')  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RelationshipTypes'


class Relationships(models.Model):
    relationshipid = models.AutoField(db_column='RelationshipID', primary_key=True)  # Field name made lowercase.
    relationshiptypeid = models.ForeignKey(Relationshiptypes, models.DO_NOTHING, db_column='RelationshipTypeID')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=500, blank=True, null=True)  # Field name made lowercase.
    portalid = models.ForeignKey(Portals, models.DO_NOTHING, db_column='PortalID', blank=True, null=True)  # Field name made lowercase.
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='UserID', blank=True, null=True)  # Field name made lowercase.
    defaultresponse = models.IntegerField(db_column='DefaultResponse')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID')  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate')  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID')  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Relationships'


class Revisions(models.Model):
    revisionid = models.AutoField(db_column='RevisionId', primary_key=True)  # Field name made lowercase.
    sequence = models.IntegerField(db_column='Sequence')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.
    contentitemid = models.IntegerField(db_column='ContentItemId')  # Field name made lowercase.
    revisiontype = models.IntegerField(db_column='RevisionType')  # Field name made lowercase.
    state = models.IntegerField(db_column='State')  # Field name made lowercase.
    changeset = models.TextField(db_column='Changeset', blank=True, null=True)  # Field name made lowercase.
    objectkey = models.CharField(db_column='ObjectKey', max_length=64, blank=True, null=True)  # Field name made lowercase.
    createduserid = models.IntegerField(db_column='CreatedUserId')  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate')  # Field name made lowercase.
    lastmodifieduserid = models.IntegerField(db_column='LastModifiedUserId')  # Field name made lowercase.
    lastmodifieddate = models.DateTimeField(db_column='LastModifiedDate')  # Field name made lowercase.
    contentitemtype = models.IntegerField(db_column='ContentItemType')  # Field name made lowercase.
    childitemid = models.IntegerField(db_column='ChildItemId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Revisions'


class RevisionsLocks(models.Model):
    lockid = models.AutoField(db_column='LockId', primary_key=True)  # Field name made lowercase.
    contentitemid = models.IntegerField(db_column='ContentItemId')  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserId')  # Field name made lowercase.
    lockeddate = models.DateTimeField(db_column='LockedDate')  # Field name made lowercase.
    contentitemtype = models.IntegerField(db_column='ContentItemType')  # Field name made lowercase.
    childitemid = models.IntegerField(db_column='ChildItemId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Revisions_Locks'


class RevisionsStatehistory(models.Model):
    revisionstateid = models.AutoField(db_column='RevisionStateId', primary_key=True)  # Field name made lowercase.
    revisionid = models.IntegerField(db_column='RevisionId')  # Field name made lowercase.
    oldstate = models.IntegerField(db_column='OldState', blank=True, null=True)  # Field name made lowercase.
    newstate = models.IntegerField(db_column='NewState')  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserId')  # Field name made lowercase.
    transitiondate = models.DateTimeField(db_column='TransitionDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Revisions_StateHistory'


class Rolegroups(models.Model):
    rolegroupid = models.AutoField(db_column='RoleGroupID', primary_key=True)  # Field name made lowercase.
    portalid = models.ForeignKey(Portals, models.DO_NOTHING, db_column='PortalID')  # Field name made lowercase.
    rolegroupname = models.CharField(db_column='RoleGroupName', max_length=50)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RoleGroups'
        unique_together = (('portalid', 'rolegroupname'),)


class Rolesettings(models.Model):
    rolesettingid = models.AutoField(db_column='RoleSettingID', primary_key=True)  # Field name made lowercase.
    roleid = models.IntegerField(db_column='RoleID')  # Field name made lowercase.
    settingname = models.CharField(db_column='SettingName', max_length=50)  # Field name made lowercase.
    settingvalue = models.CharField(db_column='SettingValue', max_length=2000)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID')  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate')  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID')  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RoleSettings'


class Roles(models.Model):
    roleid = models.AutoField(db_column='RoleID', primary_key=True)  # Field name made lowercase.
    portalid = models.ForeignKey(Portals, models.DO_NOTHING, db_column='PortalID', blank=True, null=True)  # Field name made lowercase.
    rolename = models.CharField(db_column='RoleName', max_length=50)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    servicefee = models.DecimalField(db_column='ServiceFee', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    billingfrequency = models.CharField(db_column='BillingFrequency', max_length=1, blank=True, null=True)  # Field name made lowercase.
    trialperiod = models.IntegerField(db_column='TrialPeriod', blank=True, null=True)  # Field name made lowercase.
    trialfrequency = models.CharField(db_column='TrialFrequency', max_length=1, blank=True, null=True)  # Field name made lowercase.
    billingperiod = models.IntegerField(db_column='BillingPeriod', blank=True, null=True)  # Field name made lowercase.
    trialfee = models.DecimalField(db_column='TrialFee', max_digits=19, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    ispublic = models.BooleanField(db_column='IsPublic')  # Field name made lowercase.
    autoassignment = models.BooleanField(db_column='AutoAssignment')  # Field name made lowercase.
    rolegroupid = models.ForeignKey(Rolegroups, models.DO_NOTHING, db_column='RoleGroupID', blank=True, null=True)  # Field name made lowercase.
    rsvpcode = models.CharField(db_column='RSVPCode', max_length=50, blank=True, null=True)  # Field name made lowercase.
    iconfile = models.CharField(db_column='IconFile', max_length=100, blank=True, null=True)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status')  # Field name made lowercase.
    securitymode = models.IntegerField(db_column='SecurityMode')  # Field name made lowercase.
    issystemrole = models.BooleanField(db_column='IsSystemRole')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Roles'
        unique_together = (('portalid', 'rolename'), ('portalid', 'rolename', 'roleid'), ('roleid', 'status', 'portalid', 'rolename', 'description', 'servicefee', 'billingfrequency', 'trialperiod', 'trialfrequency', 'billingperiod', 'trialfee', 'ispublic', 'autoassignment', 'rolegroupid', 'rsvpcode', 'iconfile', 'securitymode'),)


class SpconnectorConnections(models.Model):
    connectionid = models.AutoField(db_column='ConnectionId', primary_key=True)  # Field name made lowercase.
    portalid = models.ForeignKey(Portals, models.DO_NOTHING, db_column='PortalID', blank=True, null=True)  # Field name made lowercase.
    connectionname = models.CharField(db_column='ConnectionName', max_length=255)  # Field name made lowercase.
    sharepointsiteurl = models.CharField(db_column='SharePointSiteUrl', max_length=255)  # Field name made lowercase.
    sharepointversion = models.SmallIntegerField(db_column='SharePointVersion')  # Field name made lowercase.
    isanonymous = models.BooleanField(db_column='IsAnonymous')  # Field name made lowercase.
    sharepointusername = models.CharField(db_column='SharePointUserName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sharepointpassword = models.TextField(db_column='SharePointPassword', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SPConnector_Connections'


class SpconnectorListsubmissions(models.Model):
    submissionid = models.AutoField(db_column='SubmissionId', primary_key=True)  # Field name made lowercase.
    listid = models.ForeignKey('SpconnectorLists', models.DO_NOTHING, db_column='ListId')  # Field name made lowercase.
    listitemdata = models.TextField(db_column='ListItemData')  # Field name made lowercase.
    submitstatus = models.SmallIntegerField(db_column='SubmitStatus')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate')  # Field name made lowercase.
    sharepointitemid = models.IntegerField(db_column='SharePointItemId', blank=True, null=True)  # Field name made lowercase.
    sharepointlastmodified = models.DateTimeField(db_column='SharePointLastModified', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SPConnector_ListSubmissions'


class SpconnectorLists(models.Model):
    listid = models.AutoField(db_column='ListId', primary_key=True)  # Field name made lowercase.
    portalid = models.ForeignKey(Portals, models.DO_NOTHING, db_column='PortalID', blank=True, null=True)  # Field name made lowercase.
    connectionid = models.ForeignKey(SpconnectorConnections, models.DO_NOTHING, db_column='ConnectionId', blank=True, null=True)  # Field name made lowercase.
    mappingid = models.CharField(db_column='MappingId', max_length=36, blank=True, null=True)  # Field name made lowercase.
    synchtype = models.SmallIntegerField(db_column='SynchType')  # Field name made lowercase.
    listname = models.CharField(db_column='ListName', max_length=255)  # Field name made lowercase.
    viewname = models.CharField(db_column='ViewName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    listschema = models.TextField(db_column='ListSchema')  # Field name made lowercase.
    listtablename = models.CharField(db_column='ListTableName', max_length=255)  # Field name made lowercase.
    isreadonly = models.BooleanField(db_column='IsReadOnly')  # Field name made lowercase.
    lastsynchronized = models.DateTimeField(db_column='LastSynchronized', blank=True, null=True)  # Field name made lowercase.
    itemcount = models.IntegerField(db_column='ItemCount', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SPConnector_Lists'


class SpconnectorLookups(models.Model):
    lookupid = models.AutoField(db_column='LookupId', primary_key=True)  # Field name made lowercase.
    relatedlistid = models.ForeignKey(SpconnectorLists, models.DO_NOTHING, db_column='RelatedListId')  # Field name made lowercase.
    columnname = models.CharField(db_column='ColumnName', max_length=255)  # Field name made lowercase.
    sharepointlastmodified = models.DateTimeField(db_column='SharePointLastModified', blank=True, null=True)  # Field name made lowercase.
    sharepointlastmodifiedby = models.CharField(db_column='SharePointLastModifiedBy', max_length=255, blank=True, null=True)  # Field name made lowercase.
    itemid = models.IntegerField(db_column='ItemId', blank=True, null=True)  # Field name made lowercase.
    itemvalue = models.CharField(db_column='ItemValue', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SPConnector_Lookups'


class SpconnectorModulefields(models.Model):
    modulefieldid = models.AutoField(db_column='ModuleFieldId', primary_key=True)  # Field name made lowercase.
    listid = models.ForeignKey(SpconnectorLists, models.DO_NOTHING, db_column='ListId')  # Field name made lowercase.
    moduleid = models.ForeignKey(Modules, models.DO_NOTHING, db_column='ModuleId')  # Field name made lowercase.
    fieldguid = models.CharField(db_column='FieldGuid', max_length=36)  # Field name made lowercase.
    displayname = models.CharField(db_column='DisplayName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    isactive = models.NullBooleanField(db_column='IsActive')  # Field name made lowercase.
    requirederrormessage = models.CharField(db_column='RequiredErrorMessage', max_length=255, blank=True, null=True)  # Field name made lowercase.
    regex = models.CharField(db_column='Regex', max_length=255, blank=True, null=True)  # Field name made lowercase.
    regexerrormessage = models.CharField(db_column='RegexErrorMessage', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sequenceid = models.IntegerField(db_column='SequenceId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SPConnector_ModuleFields'


class Sqlqueries(models.Model):
    queryid = models.AutoField(db_column='QueryId', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=200)  # Field name made lowercase.
    query = models.TextField(db_column='Query')  # Field name made lowercase.
    connectionstringname = models.CharField(db_column='ConnectionStringName', max_length=50)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserId')  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate')  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserId')  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SQLQueries'


class Schedule(models.Model):
    scheduleid = models.AutoField(db_column='ScheduleID', primary_key=True)  # Field name made lowercase.
    typefullname = models.CharField(db_column='TypeFullName', max_length=200)  # Field name made lowercase.
    timelapse = models.IntegerField(db_column='TimeLapse')  # Field name made lowercase.
    timelapsemeasurement = models.CharField(db_column='TimeLapseMeasurement', max_length=2)  # Field name made lowercase.
    retrytimelapse = models.IntegerField(db_column='RetryTimeLapse')  # Field name made lowercase.
    retrytimelapsemeasurement = models.CharField(db_column='RetryTimeLapseMeasurement', max_length=2)  # Field name made lowercase.
    retainhistorynum = models.IntegerField(db_column='RetainHistoryNum')  # Field name made lowercase.
    attachtoevent = models.CharField(db_column='AttachToEvent', max_length=50)  # Field name made lowercase.
    catchupenabled = models.BooleanField(db_column='CatchUpEnabled')  # Field name made lowercase.
    enabled = models.BooleanField(db_column='Enabled')  # Field name made lowercase.
    objectdependencies = models.CharField(db_column='ObjectDependencies', max_length=300)  # Field name made lowercase.
    servers = models.CharField(db_column='Servers', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.
    friendlyname = models.CharField(db_column='FriendlyName', max_length=200, blank=True, null=True)  # Field name made lowercase.
    schedulestartdate = models.DateTimeField(db_column='ScheduleStartDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Schedule'


class Schedulehistory(models.Model):
    schedulehistoryid = models.AutoField(db_column='ScheduleHistoryID', primary_key=True)  # Field name made lowercase.
    scheduleid = models.ForeignKey(Schedule, models.DO_NOTHING, db_column='ScheduleID')  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='StartDate')  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    succeeded = models.NullBooleanField(db_column='Succeeded')  # Field name made lowercase.
    lognotes = models.TextField(db_column='LogNotes', blank=True, null=True)  # Field name made lowercase.
    nextstart = models.DateTimeField(db_column='NextStart', blank=True, null=True)  # Field name made lowercase.
    server = models.CharField(db_column='Server', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ScheduleHistory'


class Scheduleitemsettings(models.Model):
    scheduleid = models.OneToOneField(Schedule, models.DO_NOTHING, db_column='ScheduleID', primary_key=True)  # Field name made lowercase.
    settingname = models.CharField(db_column='SettingName', max_length=50)  # Field name made lowercase.
    settingvalue = models.TextField(db_column='SettingValue')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ScheduleItemSettings'
        unique_together = (('scheduleid', 'settingname'),)


class Searchcommonwords(models.Model):
    commonwordid = models.AutoField(db_column='CommonWordID', primary_key=True)  # Field name made lowercase.
    commonword = models.CharField(db_column='CommonWord', max_length=255)  # Field name made lowercase.
    locale = models.CharField(db_column='Locale', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SearchCommonWords'


class Searchdeleteditems(models.Model):
    searchdeleteditemsid = models.AutoField(db_column='SearchDeletedItemsID', primary_key=True)  # Field name made lowercase.
    datecreated = models.DateTimeField(db_column='DateCreated')  # Field name made lowercase.
    document = models.TextField(db_column='Document', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SearchDeletedItems'


class Searchindexer(models.Model):
    searchindexerid = models.AutoField(db_column='SearchIndexerID', primary_key=True)  # Field name made lowercase.
    searchindexerassemblyqualifiedname = models.CharField(db_column='SearchIndexerAssemblyQualifiedName', max_length=200)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SearchIndexer'


class Searchpreviousfilecrawlerrunitems(models.Model):
    fileid = models.IntegerField(db_column='FileId', primary_key=True)  # Field name made lowercase.
    searchtypeid = models.IntegerField(db_column='SearchTypeId')  # Field name made lowercase.
    scheduleid = models.IntegerField(db_column='ScheduleId')  # Field name made lowercase.
    filename = models.CharField(db_column='FileName', max_length=246)  # Field name made lowercase.
    url = models.CharField(db_column='Url', max_length=256, blank=True, null=True)  # Field name made lowercase.
    fileuniqueid = models.CharField(db_column='FileUniqueId', max_length=36, blank=True, null=True)  # Field name made lowercase.
    sha1hash = models.CharField(db_column='Sha1Hash', max_length=40, blank=True, null=True)  # Field name made lowercase.
    bodyindexed = models.BooleanField(db_column='BodyIndexed')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SearchPreviousFileCrawlerRunItems'
        unique_together = (('fileid', 'searchtypeid', 'scheduleid'),)


class Searchstopwords(models.Model):
    stopwordsid = models.AutoField(db_column='StopWordsID', primary_key=True)  # Field name made lowercase.
    stopwords = models.TextField(db_column='StopWords')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID')  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate')  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID')  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalID')  # Field name made lowercase.
    culturecode = models.CharField(db_column='CultureCode', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SearchStopWords'


class Searchtypes(models.Model):
    searchtypeid = models.AutoField(db_column='SearchTypeId', primary_key=True)  # Field name made lowercase.
    searchtypename = models.CharField(db_column='SearchTypeName', max_length=100)  # Field name made lowercase.
    searchresultclass = models.CharField(db_column='SearchResultClass', max_length=256)  # Field name made lowercase.
    isprivate = models.NullBooleanField(db_column='IsPrivate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SearchTypes'


class Sitelog(models.Model):
    sitelogid = models.AutoField(db_column='SiteLogId', primary_key=True)  # Field name made lowercase.
    datetime = models.DateTimeField(db_column='DateTime')  # Field name made lowercase.
    portalid = models.ForeignKey(Portals, models.DO_NOTHING, db_column='PortalId')  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserId', blank=True, null=True)  # Field name made lowercase.
    referrer = models.CharField(db_column='Referrer', max_length=255, blank=True, null=True)  # Field name made lowercase.
    url = models.CharField(db_column='Url', max_length=255, blank=True, null=True)  # Field name made lowercase.
    useragent = models.CharField(db_column='UserAgent', max_length=255, blank=True, null=True)  # Field name made lowercase.
    userhostaddress = models.CharField(db_column='UserHostAddress', max_length=255, blank=True, null=True)  # Field name made lowercase.
    userhostname = models.CharField(db_column='UserHostName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tabid = models.IntegerField(db_column='TabId', blank=True, null=True)  # Field name made lowercase.
    affiliateid = models.IntegerField(db_column='AffiliateId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SiteLog'


class Skincontrols(models.Model):
    skincontrolid = models.AutoField(db_column='SkinControlID', primary_key=True)  # Field name made lowercase.
    packageid = models.ForeignKey(Packages, models.DO_NOTHING, db_column='PackageID')  # Field name made lowercase.
    controlkey = models.CharField(db_column='ControlKey', max_length=50, blank=True, null=True)  # Field name made lowercase.
    controlsrc = models.CharField(db_column='ControlSrc', max_length=256, blank=True, null=True)  # Field name made lowercase.
    iconfile = models.CharField(db_column='IconFile', max_length=100, blank=True, null=True)  # Field name made lowercase.
    helpurl = models.CharField(db_column='HelpUrl', max_length=200, blank=True, null=True)  # Field name made lowercase.
    supportspartialrendering = models.BooleanField(db_column='SupportsPartialRendering')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SkinControls'


class Skinpackages(models.Model):
    skinpackageid = models.AutoField(db_column='SkinPackageID', primary_key=True)  # Field name made lowercase.
    packageid = models.ForeignKey(Packages, models.DO_NOTHING, db_column='PackageID')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalID', blank=True, null=True)  # Field name made lowercase.
    skinname = models.CharField(db_column='SkinName', max_length=50)  # Field name made lowercase.
    skintype = models.CharField(db_column='SkinType', max_length=20)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SkinPackages'


class Skins(models.Model):
    skinid = models.AutoField(db_column='SkinID', primary_key=True)  # Field name made lowercase.
    skinpackageid = models.ForeignKey(Skinpackages, models.DO_NOTHING, db_column='SkinPackageID')  # Field name made lowercase.
    skinsrc = models.CharField(db_column='SkinSrc', max_length=250)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Skins'


class Synonymsgroups(models.Model):
    synonymsgroupid = models.AutoField(db_column='SynonymsGroupID', primary_key=True)  # Field name made lowercase.
    synonymstags = models.TextField(db_column='SynonymsTags')  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalID')  # Field name made lowercase.
    culturecode = models.CharField(db_column='CultureCode', max_length=50)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID')  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate')  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID')  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SynonymsGroups'


class Systemmessages(models.Model):
    messageid = models.AutoField(db_column='MessageID', primary_key=True)  # Field name made lowercase.
    portalid = models.ForeignKey(Portals, models.DO_NOTHING, db_column='PortalID', blank=True, null=True)  # Field name made lowercase.
    messagename = models.CharField(db_column='MessageName', max_length=50)  # Field name made lowercase.
    messagevalue = models.TextField(db_column='MessageValue')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SystemMessages'
        unique_together = (('messagename', 'portalid'),)


class Tabaliasskins(models.Model):
    tabaliasskinid = models.AutoField(db_column='TabAliasSkinId', primary_key=True)  # Field name made lowercase.
    tabid = models.IntegerField(db_column='TabId')  # Field name made lowercase.
    portalaliasid = models.IntegerField(db_column='PortalAliasId')  # Field name made lowercase.
    skinsrc = models.CharField(db_column='SkinSrc', max_length=200)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserId', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserId', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TabAliasSkins'


class Tabmodulesettings(models.Model):
    tabmoduleid = models.OneToOneField('Tabmodules', models.DO_NOTHING, db_column='TabModuleID', primary_key=True)  # Field name made lowercase.
    settingname = models.CharField(db_column='SettingName', max_length=50)  # Field name made lowercase.
    settingvalue = models.TextField(db_column='SettingValue')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TabModuleSettings'
        unique_together = (('tabmoduleid', 'settingname'),)


class Tabmodules(models.Model):
    tabmoduleid = models.AutoField(db_column='TabModuleID', primary_key=True)  # Field name made lowercase.
    tabid = models.ForeignKey('Tabs', models.DO_NOTHING, db_column='TabID')  # Field name made lowercase.
    moduleid = models.ForeignKey(Modules, models.DO_NOTHING, db_column='ModuleID')  # Field name made lowercase.
    panename = models.CharField(db_column='PaneName', max_length=50)  # Field name made lowercase.
    moduleorder = models.IntegerField(db_column='ModuleOrder')  # Field name made lowercase.
    cachetime = models.IntegerField(db_column='CacheTime')  # Field name made lowercase.
    alignment = models.CharField(db_column='Alignment', max_length=10, blank=True, null=True)  # Field name made lowercase.
    color = models.CharField(db_column='Color', max_length=20, blank=True, null=True)  # Field name made lowercase.
    border = models.CharField(db_column='Border', max_length=1, blank=True, null=True)  # Field name made lowercase.
    iconfile = models.CharField(db_column='IconFile', max_length=100, blank=True, null=True)  # Field name made lowercase.
    visibility = models.IntegerField(db_column='Visibility')  # Field name made lowercase.
    containersrc = models.CharField(db_column='ContainerSrc', max_length=200, blank=True, null=True)  # Field name made lowercase.
    displaytitle = models.BooleanField(db_column='DisplayTitle')  # Field name made lowercase.
    displayprint = models.BooleanField(db_column='DisplayPrint')  # Field name made lowercase.
    displaysyndicate = models.BooleanField(db_column='DisplaySyndicate')  # Field name made lowercase.
    iswebslice = models.BooleanField(db_column='IsWebSlice')  # Field name made lowercase.
    webslicetitle = models.CharField(db_column='WebSliceTitle', max_length=256, blank=True, null=True)  # Field name made lowercase.
    websliceexpirydate = models.DateTimeField(db_column='WebSliceExpiryDate', blank=True, null=True)  # Field name made lowercase.
    webslicettl = models.IntegerField(db_column='WebSliceTTL', blank=True, null=True)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.BooleanField(db_column='IsDeleted')  # Field name made lowercase.
    cachemethod = models.CharField(db_column='CacheMethod', max_length=50, blank=True, null=True)  # Field name made lowercase.
    moduletitle = models.CharField(db_column='ModuleTitle', max_length=256, blank=True, null=True)  # Field name made lowercase.
    header = models.TextField(db_column='Header', blank=True, null=True)  # Field name made lowercase.
    footer = models.TextField(db_column='Footer', blank=True, null=True)  # Field name made lowercase.
    culturecode = models.CharField(db_column='CultureCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    uniqueid = models.CharField(db_column='UniqueId', unique=True, max_length=36)  # Field name made lowercase.
    versionguid = models.CharField(db_column='VersionGuid', max_length=36)  # Field name made lowercase.
    defaultlanguageguid = models.CharField(db_column='DefaultLanguageGuid', max_length=36, blank=True, null=True)  # Field name made lowercase.
    localizedversionguid = models.CharField(db_column='LocalizedVersionGuid', max_length=36)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TabModules'
        unique_together = (('tabid', 'moduleid', 'isdeleted', 'culturecode', 'moduletitle'),)


class Tabpermission(models.Model):
    tabpermissionid = models.AutoField(db_column='TabPermissionID', primary_key=True)  # Field name made lowercase.
    tabid = models.ForeignKey('Tabs', models.DO_NOTHING, db_column='TabID')  # Field name made lowercase.
    permissionid = models.ForeignKey(Permission, models.DO_NOTHING, db_column='PermissionID')  # Field name made lowercase.
    allowaccess = models.BooleanField(db_column='AllowAccess')  # Field name made lowercase.
    roleid = models.ForeignKey(Roles, models.DO_NOTHING, db_column='RoleID', blank=True, null=True)  # Field name made lowercase.
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='UserID', blank=True, null=True)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TabPermission'
        unique_together = (('tabid', 'permissionid', 'roleid', 'userid', 'allowaccess'), ('roleid', 'tabid', 'permissionid', 'allowaccess'), ('userid', 'tabid', 'permissionid', 'allowaccess'),)


class Tabsettings(models.Model):
    tabid = models.OneToOneField('Tabs', models.DO_NOTHING, db_column='TabID', primary_key=True)  # Field name made lowercase.
    settingname = models.CharField(db_column='SettingName', max_length=50)  # Field name made lowercase.
    settingvalue = models.CharField(db_column='SettingValue', max_length=2000)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TabSettings'
        unique_together = (('tabid', 'settingname'), ('tabid', 'settingname'),)


class Taburls(models.Model):
    tabid = models.OneToOneField('Tabs', models.DO_NOTHING, db_column='TabId', primary_key=True)  # Field name made lowercase.
    seqnum = models.IntegerField(db_column='SeqNum')  # Field name made lowercase.
    url = models.CharField(db_column='Url', max_length=200)  # Field name made lowercase.
    querystring = models.CharField(db_column='QueryString', max_length=200, blank=True, null=True)  # Field name made lowercase.
    httpstatus = models.CharField(db_column='HttpStatus', max_length=50)  # Field name made lowercase.
    culturecode = models.CharField(db_column='CultureCode', max_length=50, blank=True, null=True)  # Field name made lowercase.
    issystem = models.BooleanField(db_column='IsSystem')  # Field name made lowercase.
    portalaliasid = models.IntegerField(db_column='PortalAliasId', blank=True, null=True)  # Field name made lowercase.
    portalaliasusage = models.IntegerField(db_column='PortalAliasUsage', blank=True, null=True)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TabUrls'
        unique_together = (('tabid', 'seqnum'),)


class Tabversiondetails(models.Model):
    tabversiondetailid = models.AutoField(db_column='TabVersionDetailId', primary_key=True)  # Field name made lowercase.
    tabversionid = models.ForeignKey('Tabversions', models.DO_NOTHING, db_column='TabVersionId')  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId')  # Field name made lowercase.
    moduleversion = models.IntegerField(db_column='ModuleVersion')  # Field name made lowercase.
    panename = models.CharField(db_column='PaneName', max_length=50)  # Field name made lowercase.
    moduleorder = models.IntegerField(db_column='ModuleOrder')  # Field name made lowercase.
    action = models.IntegerField(db_column='Action')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID')  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate')  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID')  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TabVersionDetails'
        unique_together = (('tabversionid', 'moduleid'),)


class Tabversions(models.Model):
    tabversionid = models.AutoField(db_column='TabVersionId', primary_key=True)  # Field name made lowercase.
    tabid = models.ForeignKey('Tabs', models.DO_NOTHING, db_column='TabId')  # Field name made lowercase.
    version = models.IntegerField(db_column='Version')  # Field name made lowercase.
    timestamp = models.DateTimeField(db_column='TimeStamp')  # Field name made lowercase.
    ispublished = models.BooleanField(db_column='IsPublished')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID')  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate')  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID')  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TabVersions'
        unique_together = (('tabid', 'version'),)


class Tabs(models.Model):
    tabid = models.AutoField(db_column='TabID', primary_key=True)  # Field name made lowercase.
    taborder = models.IntegerField(db_column='TabOrder')  # Field name made lowercase.
    portalid = models.ForeignKey(Portals, models.DO_NOTHING, db_column='PortalID', blank=True, null=True)  # Field name made lowercase.
    tabname = models.CharField(db_column='TabName', max_length=200)  # Field name made lowercase.
    isvisible = models.BooleanField(db_column='IsVisible')  # Field name made lowercase.
    parentid = models.ForeignKey('self', models.DO_NOTHING, db_column='ParentId', blank=True, null=True)  # Field name made lowercase.
    iconfile = models.CharField(db_column='IconFile', max_length=255, blank=True, null=True)  # Field name made lowercase.
    disablelink = models.BooleanField(db_column='DisableLink')  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=200, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=500, blank=True, null=True)  # Field name made lowercase.
    keywords = models.CharField(db_column='KeyWords', max_length=500, blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.BooleanField(db_column='IsDeleted')  # Field name made lowercase.
    url = models.CharField(db_column='Url', max_length=255, blank=True, null=True)  # Field name made lowercase.
    skinsrc = models.CharField(db_column='SkinSrc', max_length=200, blank=True, null=True)  # Field name made lowercase.
    containersrc = models.CharField(db_column='ContainerSrc', max_length=200, blank=True, null=True)  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='StartDate', blank=True, null=True)  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    refreshinterval = models.IntegerField(db_column='RefreshInterval', blank=True, null=True)  # Field name made lowercase.
    pageheadtext = models.TextField(db_column='PageHeadText', blank=True, null=True)  # Field name made lowercase.
    issecure = models.BooleanField(db_column='IsSecure')  # Field name made lowercase.
    permanentredirect = models.BooleanField(db_column='PermanentRedirect')  # Field name made lowercase.
    sitemappriority = models.FloatField(db_column='SiteMapPriority')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.
    iconfilelarge = models.CharField(db_column='IconFileLarge', max_length=255, blank=True, null=True)  # Field name made lowercase.
    culturecode = models.CharField(db_column='CultureCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    contentitemid = models.ForeignKey(Contentitems, models.DO_NOTHING, db_column='ContentItemID', blank=True, null=True)  # Field name made lowercase.
    uniqueid = models.CharField(db_column='UniqueId', unique=True, max_length=36)  # Field name made lowercase.
    versionguid = models.CharField(db_column='VersionGuid', max_length=36)  # Field name made lowercase.
    defaultlanguageguid = models.CharField(db_column='DefaultLanguageGuid', max_length=36, blank=True, null=True)  # Field name made lowercase.
    localizedversionguid = models.CharField(db_column='LocalizedVersionGuid', max_length=36)  # Field name made lowercase.
    level = models.IntegerField(db_column='Level')  # Field name made lowercase.
    tabpath = models.CharField(db_column='TabPath', max_length=255)  # Field name made lowercase.
    hasbeenpublished = models.BooleanField(db_column='HasBeenPublished')  # Field name made lowercase.
    issystem = models.BooleanField(db_column='IsSystem')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tabs'


class TaxonomyScopetypes(models.Model):
    scopetypeid = models.AutoField(db_column='ScopeTypeID', primary_key=True)  # Field name made lowercase.
    scopetype = models.CharField(db_column='ScopeType', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Taxonomy_ScopeTypes'


class TaxonomyTerms(models.Model):
    termid = models.AutoField(db_column='TermID', primary_key=True)  # Field name made lowercase.
    vocabularyid = models.ForeignKey('TaxonomyVocabularies', models.DO_NOTHING, db_column='VocabularyID')  # Field name made lowercase.
    parenttermid = models.ForeignKey('self', models.DO_NOTHING, db_column='ParentTermID', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=250)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=2500, blank=True, null=True)  # Field name made lowercase.
    weight = models.IntegerField(db_column='Weight')  # Field name made lowercase.
    termleft = models.IntegerField(db_column='TermLeft')  # Field name made lowercase.
    termright = models.IntegerField(db_column='TermRight')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Taxonomy_Terms'


class TaxonomyVocabularies(models.Model):
    vocabularyid = models.AutoField(db_column='VocabularyID', primary_key=True)  # Field name made lowercase.
    vocabularytypeid = models.ForeignKey('TaxonomyVocabularytypes', models.DO_NOTHING, db_column='VocabularyTypeID')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=250)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=2500, blank=True, null=True)  # Field name made lowercase.
    weight = models.IntegerField(db_column='Weight')  # Field name made lowercase.
    scopeid = models.IntegerField(db_column='ScopeID', blank=True, null=True)  # Field name made lowercase.
    scopetypeid = models.ForeignKey(TaxonomyScopetypes, models.DO_NOTHING, db_column='ScopeTypeID')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.
    issystem = models.BooleanField(db_column='IsSystem')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Taxonomy_Vocabularies'


class TaxonomyVocabularytypes(models.Model):
    vocabularytypeid = models.AutoField(db_column='VocabularyTypeID', primary_key=True)  # Field name made lowercase.
    vocabularytype = models.CharField(db_column='VocabularyType', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Taxonomy_VocabularyTypes'


class Urllog(models.Model):
    urllogid = models.AutoField(db_column='UrlLogID', primary_key=True)  # Field name made lowercase.
    urltrackingid = models.ForeignKey('Urltracking', models.DO_NOTHING, db_column='UrlTrackingID')  # Field name made lowercase.
    clickdate = models.DateTimeField(db_column='ClickDate')  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UrlLog'


class Urltracking(models.Model):
    urltrackingid = models.AutoField(db_column='UrlTrackingID', primary_key=True)  # Field name made lowercase.
    portalid = models.ForeignKey(Portals, models.DO_NOTHING, db_column='PortalID', blank=True, null=True)  # Field name made lowercase.
    url = models.CharField(db_column='Url', max_length=255)  # Field name made lowercase.
    urltype = models.CharField(db_column='UrlType', max_length=1)  # Field name made lowercase.
    clicks = models.IntegerField(db_column='Clicks')  # Field name made lowercase.
    lastclick = models.DateTimeField(db_column='LastClick', blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate')  # Field name made lowercase.
    logactivity = models.BooleanField(db_column='LogActivity')  # Field name made lowercase.
    trackclicks = models.BooleanField(db_column='TrackClicks')  # Field name made lowercase.
    moduleid = models.IntegerField(db_column='ModuleId', blank=True, null=True)  # Field name made lowercase.
    newwindow = models.BooleanField(db_column='NewWindow')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UrlTracking'
        unique_together = (('portalid', 'url', 'moduleid'),)


class Urls(models.Model):
    urlid = models.AutoField(db_column='UrlID', primary_key=True)  # Field name made lowercase.
    portalid = models.ForeignKey(Portals, models.DO_NOTHING, db_column='PortalID', blank=True, null=True)  # Field name made lowercase.
    url = models.CharField(db_column='Url', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Urls'
        unique_together = (('url', 'portalid'),)


class Userauthentication(models.Model):
    userauthenticationid = models.AutoField(db_column='UserAuthenticationID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='UserID')  # Field name made lowercase.
    authenticationtype = models.CharField(db_column='AuthenticationType', max_length=100)  # Field name made lowercase.
    authenticationtoken = models.CharField(db_column='AuthenticationToken', max_length=1000)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserAuthentication'
        unique_together = (('userid', 'authenticationtype'),)


class Userdefineddata(models.Model):
    userdefinedfieldid = models.OneToOneField('Userdefinedfields', models.DO_NOTHING, db_column='UserDefinedFieldId', primary_key=True)  # Field name made lowercase.
    userdefinedrowid = models.ForeignKey('Userdefinedrows', models.DO_NOTHING, db_column='UserDefinedRowId')  # Field name made lowercase.
    fieldvalue = models.TextField(db_column='FieldValue', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserDefinedData'
        unique_together = (('userdefinedfieldid', 'userdefinedrowid'),)


class Userdefinedfieldsettings(models.Model):
    fieldid = models.OneToOneField('Userdefinedfields', models.DO_NOTHING, db_column='FieldId', primary_key=True)  # Field name made lowercase.
    settingname = models.CharField(db_column='SettingName', max_length=50)  # Field name made lowercase.
    settingvalue = models.TextField(db_column='SettingValue', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserDefinedFieldSettings'
        unique_together = (('fieldid', 'settingname'),)


class Userdefinedfields(models.Model):
    userdefinedfieldid = models.AutoField(db_column='UserDefinedFieldId', primary_key=True)  # Field name made lowercase.
    moduleid = models.ForeignKey(Modules, models.DO_NOTHING, db_column='ModuleId')  # Field name made lowercase.
    fieldtitle = models.CharField(db_column='FieldTitle', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    visible = models.BooleanField(db_column='Visible')  # Field name made lowercase.
    fieldorder = models.IntegerField(db_column='FieldOrder')  # Field name made lowercase.
    fieldtype = models.CharField(db_column='FieldType', max_length=20)  # Field name made lowercase.
    required = models.BooleanField(db_column='Required')  # Field name made lowercase.
    default = models.CharField(db_column='Default', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    outputsettings = models.CharField(db_column='OutputSettings', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    inputsettings = models.TextField(db_column='InputSettings', blank=True, null=True)  # Field name made lowercase.
    validationrule = models.CharField(db_column='ValidationRule', max_length=512, blank=True, null=True)  # Field name made lowercase.
    validationmessage = models.CharField(db_column='ValidationMessage', max_length=512, blank=True, null=True)  # Field name made lowercase.
    normalizeflag = models.BooleanField(db_column='NormalizeFlag')  # Field name made lowercase.
    helptext = models.TextField(db_column='HelpText', blank=True, null=True)  # Field name made lowercase.
    searchable = models.BooleanField(db_column='Searchable')  # Field name made lowercase.
    showonedit = models.BooleanField(db_column='ShowOnEdit')  # Field name made lowercase.
    privatefield = models.BooleanField(db_column='PrivateField')  # Field name made lowercase.
    editstyle = models.CharField(db_column='EditStyle', max_length=512, blank=True, null=True)  # Field name made lowercase.
    multiplevalues = models.BooleanField(db_column='MultipleValues')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserDefinedFields'
        unique_together = (('moduleid', 'fieldorder'),)


class Userdefinedrows(models.Model):
    userdefinedrowid = models.AutoField(db_column='UserDefinedRowId', primary_key=True)  # Field name made lowercase.
    moduleid = models.ForeignKey(Modules, models.DO_NOTHING, db_column='ModuleId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserDefinedRows'


class Userportals(models.Model):
    # userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='UserId', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='UserId')  # Field name made lowercase.
    portalid = models.ForeignKey(Portals, models.DO_NOTHING, db_column='PortalId')  # Field name made lowercase.
    userportalid = models.AutoField(db_column='UserPortalId', primary_key=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate')  # Field name made lowercase.
    authorised = models.BooleanField(db_column='Authorised')  # Field name made lowercase.
    isdeleted = models.BooleanField(db_column='IsDeleted')  # Field name made lowercase.
    refreshroles = models.BooleanField(db_column='RefreshRoles')  # Field name made lowercase.
    vanityurl = models.CharField(db_column='VanityUrl', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserPortals'
        unique_together = (('userid', 'portalid'),)


class Userprofile(models.Model):
    profileid = models.AutoField(db_column='ProfileID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='UserID')  # Field name made lowercase.
    propertydefinitionid = models.ForeignKey(Profilepropertydefinition, models.DO_NOTHING, db_column='PropertyDefinitionID')  # Field name made lowercase.
    propertyvalue = models.CharField(db_column='PropertyValue', max_length=3750, blank=True, null=True)  # Field name made lowercase.
    propertytext = models.TextField(db_column='PropertyText', blank=True, null=True)  # Field name made lowercase.
    visibility = models.IntegerField(db_column='Visibility')  # Field name made lowercase.
    lastupdateddate = models.DateTimeField(db_column='LastUpdatedDate')  # Field name made lowercase.
    extendedvisibility = models.CharField(db_column='ExtendedVisibility', max_length=400, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserProfile'


class Userrelationshippreferences(models.Model):
    preferenceid = models.AutoField(db_column='PreferenceID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='UserID')  # Field name made lowercase.
    relationshipid = models.ForeignKey(Relationships, models.DO_NOTHING, db_column='RelationshipID')  # Field name made lowercase.
    defaultresponse = models.IntegerField(db_column='DefaultResponse')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID')  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate')  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID')  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserRelationshipPreferences'
        unique_together = (('preferenceid', 'relationshipid'),)


class Userrelationships(models.Model):
    userrelationshipid = models.AutoField(db_column='UserRelationshipID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='UserID', related_name='user')  # Field name made lowercase.
    relateduserid = models.ForeignKey('Users', models.DO_NOTHING, db_column='RelatedUserID', related_name='related_user')  # Field name made lowercase.
    relationshipid = models.ForeignKey(Relationships, models.DO_NOTHING, db_column='RelationshipID')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID')  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate')  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID')  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserRelationships'
        unique_together = (('userid', 'relateduserid', 'relationshipid'),)


class Userroles(models.Model):
    userroleid = models.AutoField(db_column='UserRoleID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='UserID')  # Field name made lowercase.
    roleid = models.ForeignKey(Roles, models.DO_NOTHING, db_column='RoleID')  # Field name made lowercase.
    expirydate = models.DateTimeField(db_column='ExpiryDate', blank=True, null=True)  # Field name made lowercase.
    istrialused = models.NullBooleanField(db_column='IsTrialUsed')  # Field name made lowercase.
    effectivedate = models.DateTimeField(db_column='EffectiveDate', blank=True, null=True)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status')  # Field name made lowercase.
    isowner = models.BooleanField(db_column='IsOwner')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserRoles'
        unique_together = (('roleid', 'userid'), ('userid', 'roleid'), ('roleid', 'userid', 'userroleid', 'expirydate', 'istrialused', 'effectivedate', 'createdbyuserid', 'createdondate', 'lastmodifiedbyuserid', 'lastmodifiedondate', 'status', 'isowner'),)


class Users(models.Model):
    userid = models.AutoField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='Username', unique=True, max_length=100)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=50)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=50)  # Field name made lowercase.
    issuperuser = models.BooleanField(db_column='IsSuperUser')  # Field name made lowercase.
    affiliateid = models.IntegerField(db_column='AffiliateId', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=256, blank=True, null=True)  # Field name made lowercase.
    displayname = models.CharField(db_column='DisplayName', max_length=128)  # Field name made lowercase.
    updatepassword = models.BooleanField(db_column='UpdatePassword')  # Field name made lowercase.
    lastipaddress = models.CharField(db_column='LastIPAddress', max_length=50, blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.BooleanField(db_column='IsDeleted')  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.
    passwordresettoken = models.CharField(db_column='PasswordResetToken', max_length=36, blank=True, null=True)  # Field name made lowercase.
    passwordresetexpiration = models.DateTimeField(db_column='PasswordResetExpiration', blank=True, null=True)  # Field name made lowercase.
    loweremail = models.CharField(db_column='LowerEmail', max_length=256, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Users'
        unique_together = (('username', 'userid', 'firstname', 'lastname', 'issuperuser', 'affiliateid', 'email', 'displayname', 'updatepassword', 'lastipaddress', 'isdeleted', 'createdbyuserid', 'createdondate', 'lastmodifiedbyuserid', 'lastmodifiedondate', 'passwordresettoken', 'passwordresetexpiration'),)


class Usersonline(models.Model):
    userid = models.OneToOneField(Users, models.DO_NOTHING, db_column='UserID', primary_key=True)  # Field name made lowercase.
    portalid = models.ForeignKey(Portals, models.DO_NOTHING, db_column='PortalID')  # Field name made lowercase.
    tabid = models.IntegerField(db_column='TabID')  # Field name made lowercase.
    creationdate = models.DateTimeField(db_column='CreationDate')  # Field name made lowercase.
    lastactivedate = models.DateTimeField(db_column='LastActiveDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UsersOnline'
        unique_together = (('userid', 'portalid'),)


class Vendorclassification(models.Model):
    vendorclassificationid = models.AutoField(db_column='VendorClassificationId', primary_key=True)  # Field name made lowercase.
    vendorid = models.ForeignKey('Vendors', models.DO_NOTHING, db_column='VendorId')  # Field name made lowercase.
    classificationid = models.ForeignKey(Classification, models.DO_NOTHING, db_column='ClassificationId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'VendorClassification'
        unique_together = (('vendorid', 'classificationid'),)


class Vendors(models.Model):
    vendorid = models.AutoField(db_column='VendorId', primary_key=True)  # Field name made lowercase.
    vendorname = models.CharField(db_column='VendorName', max_length=50)  # Field name made lowercase.
    street = models.CharField(db_column='Street', max_length=50, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=50, blank=True, null=True)  # Field name made lowercase.
    region = models.CharField(db_column='Region', max_length=50, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=50, blank=True, null=True)  # Field name made lowercase.
    postalcode = models.CharField(db_column='PostalCode', max_length=50, blank=True, null=True)  # Field name made lowercase.
    telephone = models.CharField(db_column='Telephone', max_length=50, blank=True, null=True)  # Field name made lowercase.
    portalid = models.ForeignKey(Portals, models.DO_NOTHING, db_column='PortalId', blank=True, null=True)  # Field name made lowercase.
    fax = models.CharField(db_column='Fax', max_length=50, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=50, blank=True, null=True)  # Field name made lowercase.
    website = models.CharField(db_column='Website', max_length=100, blank=True, null=True)  # Field name made lowercase.
    clickthroughs = models.IntegerField(db_column='ClickThroughs')  # Field name made lowercase.
    views = models.IntegerField(db_column='Views')  # Field name made lowercase.
    createdbyuser = models.CharField(db_column='CreatedByUser', max_length=100, blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate', blank=True, null=True)  # Field name made lowercase.
    logofile = models.CharField(db_column='LogoFile', max_length=100, blank=True, null=True)  # Field name made lowercase.
    keywords = models.TextField(db_column='KeyWords', blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=50, blank=True, null=True)  # Field name made lowercase.
    authorized = models.BooleanField(db_column='Authorized')  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cell = models.CharField(db_column='Cell', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Vendors'
        unique_together = (('portalid', 'vendorname'),)


class Version(models.Model):
    versionid = models.AutoField(db_column='VersionId', primary_key=True)  # Field name made lowercase.
    major = models.IntegerField(db_column='Major')  # Field name made lowercase.
    minor = models.IntegerField(db_column='Minor')  # Field name made lowercase.
    build = models.IntegerField(db_column='Build')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate')  # Field name made lowercase.
    increment = models.IntegerField(db_column='Increment', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Version'
        unique_together = (('major', 'minor', 'build', 'increment'),)


class Webservers(models.Model):
    serverid = models.AutoField(db_column='ServerID', primary_key=True)  # Field name made lowercase.
    servername = models.CharField(db_column='ServerName', max_length=50)  # Field name made lowercase.
    createddate = models.DateTimeField(db_column='CreatedDate')  # Field name made lowercase.
    lastactivitydate = models.DateTimeField(db_column='LastActivityDate')  # Field name made lowercase.
    url = models.CharField(db_column='URL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    iisappname = models.CharField(db_column='IISAppName', max_length=200)  # Field name made lowercase.
    enabled = models.BooleanField(db_column='Enabled')  # Field name made lowercase.
    servergroup = models.CharField(db_column='ServerGroup', max_length=200, blank=True, null=True)  # Field name made lowercase.
    uniqueid = models.CharField(db_column='UniqueId', max_length=200, blank=True, null=True)  # Field name made lowercase.
    pingfailurecount = models.IntegerField(db_column='PingFailureCount')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'WebServers'
        unique_together = (('servername', 'iisappname'),)


class Workflow(models.Model):
    workflowid = models.AutoField(db_column='WorkflowID', primary_key=True)  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalID', blank=True, null=True)  # Field name made lowercase.
    workflowname = models.CharField(db_column='WorkflowName', max_length=50)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    isdeleted = models.BooleanField(db_column='IsDeleted')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Workflow'
        unique_together = (('portalid', 'workflowname'),)


class Workflowmigrationmatches(models.Model):
    portalid = models.IntegerField(db_column='PortalID', primary_key=True)  # Field name made lowercase.
    oldworkflowid = models.IntegerField(db_column='OldWorkflowID')  # Field name made lowercase.
    newworkflowid = models.IntegerField(db_column='NewWorkflowID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'WorkflowMigrationMatches'
        unique_together = (('portalid', 'oldworkflowid'),)


class Workflowstatepermission(models.Model):
    workflowstatepermissionid = models.AutoField(db_column='WorkflowStatePermissionID', primary_key=True)  # Field name made lowercase.
    stateid = models.ForeignKey('Workflowstates', models.DO_NOTHING, db_column='StateID')  # Field name made lowercase.
    permissionid = models.ForeignKey(Permission, models.DO_NOTHING, db_column='PermissionID')  # Field name made lowercase.
    allowaccess = models.BooleanField(db_column='AllowAccess')  # Field name made lowercase.
    roleid = models.IntegerField(db_column='RoleID', blank=True, null=True)  # Field name made lowercase.
    userid = models.ForeignKey(Users, models.DO_NOTHING, db_column='UserID', blank=True, null=True)  # Field name made lowercase.
    createdbyuserid = models.IntegerField(db_column='CreatedByUserID', blank=True, null=True)  # Field name made lowercase.
    createdondate = models.DateTimeField(db_column='CreatedOnDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedbyuserid = models.IntegerField(db_column='LastModifiedByUserID', blank=True, null=True)  # Field name made lowercase.
    lastmodifiedondate = models.DateTimeField(db_column='LastModifiedOnDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'WorkflowStatePermission'
        unique_together = (('stateid', 'permissionid', 'roleid', 'userid'),)


class Workflowstates(models.Model):
    stateid = models.AutoField(db_column='StateID', primary_key=True)  # Field name made lowercase.
    workflowid = models.ForeignKey(Workflow, models.DO_NOTHING, db_column='WorkflowID')  # Field name made lowercase.
    statename = models.CharField(db_column='StateName', max_length=50)  # Field name made lowercase.
    order = models.IntegerField(db_column='Order')  # Field name made lowercase.
    isactive = models.BooleanField(db_column='IsActive')  # Field name made lowercase.
    notify = models.BooleanField(db_column='Notify')  # Field name made lowercase.
    notifyadmin = models.BooleanField(db_column='NotifyAdmin')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'WorkflowStates'
        unique_together = (('workflowid', 'statename'),)


class AspnetApplications(models.Model):
    applicationname = models.CharField(db_column='ApplicationName', unique=True, max_length=256)  # Field name made lowercase.
    loweredapplicationname = models.CharField(db_column='LoweredApplicationName', unique=True, max_length=256)  # Field name made lowercase.
    applicationid = models.CharField(db_column='ApplicationId', primary_key=True, max_length=36)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=256, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aspnet_Applications'


class AspnetMembership(models.Model):
    applicationid = models.ForeignKey(AspnetApplications, models.DO_NOTHING, db_column='ApplicationId')  # Field name made lowercase.
    userid = models.OneToOneField('AspnetUsers', models.DO_NOTHING, db_column='UserId', primary_key=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=128)  # Field name made lowercase.
    passwordformat = models.IntegerField(db_column='PasswordFormat')  # Field name made lowercase.
    passwordsalt = models.CharField(db_column='PasswordSalt', max_length=128)  # Field name made lowercase.
    mobilepin = models.CharField(db_column='MobilePIN', max_length=16, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=256, blank=True, null=True)  # Field name made lowercase.
    loweredemail = models.CharField(db_column='LoweredEmail', max_length=256, blank=True, null=True)  # Field name made lowercase.
    passwordquestion = models.CharField(db_column='PasswordQuestion', max_length=256, blank=True, null=True)  # Field name made lowercase.
    passwordanswer = models.CharField(db_column='PasswordAnswer', max_length=128, blank=True, null=True)  # Field name made lowercase.
    isapproved = models.BooleanField(db_column='IsApproved')  # Field name made lowercase.
    islockedout = models.BooleanField(db_column='IsLockedOut')  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='CreateDate')  # Field name made lowercase.
    lastlogindate = models.DateTimeField(db_column='LastLoginDate')  # Field name made lowercase.
    lastpasswordchangeddate = models.DateTimeField(db_column='LastPasswordChangedDate')  # Field name made lowercase.
    lastlockoutdate = models.DateTimeField(db_column='LastLockoutDate')  # Field name made lowercase.
    failedpasswordattemptcount = models.IntegerField(db_column='FailedPasswordAttemptCount')  # Field name made lowercase.
    failedpasswordattemptwindowstart = models.DateTimeField(db_column='FailedPasswordAttemptWindowStart')  # Field name made lowercase.
    failedpasswordanswerattemptcount = models.IntegerField(db_column='FailedPasswordAnswerAttemptCount')  # Field name made lowercase.
    failedpasswordanswerattemptwindowstart = models.DateTimeField(db_column='FailedPasswordAnswerAttemptWindowStart')  # Field name made lowercase.
    comment = models.TextField(db_column='Comment', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aspnet_Membership'


class AspnetSchemaversions(models.Model):
    feature = models.CharField(db_column='Feature', primary_key=True, max_length=128)  # Field name made lowercase.
    compatibleschemaversion = models.CharField(db_column='CompatibleSchemaVersion', max_length=128)  # Field name made lowercase.
    iscurrentversion = models.BooleanField(db_column='IsCurrentVersion')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aspnet_SchemaVersions'
        unique_together = (('feature', 'compatibleschemaversion'),)


class AspnetUsers(models.Model):
    applicationid = models.ForeignKey(AspnetApplications, models.DO_NOTHING, db_column='ApplicationId')  # Field name made lowercase.
    userid = models.CharField(db_column='UserId', primary_key=True, max_length=36)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=256)  # Field name made lowercase.
    loweredusername = models.CharField(db_column='LoweredUserName', max_length=256)  # Field name made lowercase.
    mobilealias = models.CharField(db_column='MobileAlias', max_length=16, blank=True, null=True)  # Field name made lowercase.
    isanonymous = models.BooleanField(db_column='IsAnonymous')  # Field name made lowercase.
    lastactivitydate = models.DateTimeField(db_column='LastActivityDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aspnet_Users'
        unique_together = (('applicationid', 'loweredusername'),)


class ScUrl(models.Model):
    urlid = models.AutoField(db_column='UrlId', primary_key=True)  # Field name made lowercase.
    url = models.CharField(db_column='Url', max_length=256, blank=True, null=True)  # Field name made lowercase.
    urlactive = models.NullBooleanField(db_column='UrlActive')  # Field name made lowercase.
    urldnnrole = models.CharField(db_column='UrlDNNRole', max_length=50, blank=True, null=True)  # Field name made lowercase.
    urldnnuser = models.CharField(db_column='UrlDNNUser', max_length=50, blank=True, null=True)  # Field name made lowercase.
    urlwinauthentication = models.NullBooleanField(db_column='UrlWinAuthentication')  # Field name made lowercase.
    urlwindomain = models.CharField(db_column='UrlWinDomain', max_length=50, blank=True, null=True)  # Field name made lowercase.
    urlwinuser = models.CharField(db_column='UrlWinUser', max_length=50, blank=True, null=True)  # Field name made lowercase.
    urlwinpassword = models.CharField(db_column='UrlWinPassword', max_length=50, blank=True, null=True)  # Field name made lowercase.
    urlsitemap = models.CharField(db_column='UrlSitemap', max_length=256, blank=True, null=True)  # Field name made lowercase.
    portalid = models.IntegerField(db_column='PortalId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sc_Url'


class Sysdiagrams(models.Model):
    name = models.CharField(max_length=128)
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)
