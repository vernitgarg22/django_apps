from django.db import models
from django.utils import timezone


class MessengerClient(models.Model):

    app_label = 'messenger'

    name = models.CharField('Name', max_length=64)
    description = models.CharField('Description', max_length=2048)
    confirmation_message = models.CharField('Confirmation Message', max_length=2048)


class MessengerPhoneNumber(models.Model):

    app_label = 'messenger'

    messenger_client = models.ForeignKey(MessengerClient, on_delete=models.PROTECT)
    phone_number = models.CharField('Phone Number', max_length=10, db_index=True, unique=True)
    description = models.CharField('Description', max_length=512, blank=True, null=True)


class MessengerNotification(models.Model):

    app_label = 'messenger'

    messenger_client = models.ForeignKey(MessengerClient, on_delete=models.PROTECT)

    # REVIEW allow day to be null to indicate 'every day' ?
    # REVIEW allow day to be a full timestamp?
    day = models.DateField('Day on which notification should be sent')
    message = models.CharField('Message', max_length=2048, blank=True, null=True)
    geo_layer_url = models.CharField('Geo Layer URL', max_length=1024, blank=True, null=True)
    formatter = models.CharField('Formatter class to render message', max_length=64, blank=True, null=True)


# "https://services2.arcgis.com/qvkbeam7Wirps6zC/arcgis/rest/services/Elections_2019/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry=-82.9988157%2C+42.351591&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=true&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pjson&token="
# "https://services2.arcgis.com/qvkbeam7Wirps6zC/arcgis/rest/services/Elections_2019/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry={lng}%2C+{lat}&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=true&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pjson&token="


class MessengerSubscriber(models.Model):

    app_label = 'messenger'

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    messenger_client = models.ForeignKey(MessengerClient, on_delete=models.PROTECT)
    phone_number = models.CharField('Subscriber phone number', unique=True, max_length=32)
    status = models.CharField('Subscriber status', max_length=32, choices=STATUS_CHOICES, default='inactive')
    address = models.CharField('Home address', max_length=128)
    latitude = models.CharField('Latitude', max_length=32)
    longitude = models.CharField('Longitude', max_length=32)
    created_at = models.DateTimeField('Time of initial subscription', default=timezone.now())
    last_status_update = models.DateTimeField('Time of last status change', default=timezone.now())

    # REVIEW TODO override save() to update latitude / longitude based on subscriber's address, as
    # well as created_at / last_status_update
