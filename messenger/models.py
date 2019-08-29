from django.db import models
from django.utils import timezone

from cod_utils.util import geocode_address, date_json


class MessengerClient(models.Model):

    app_label = 'messenger'

    name = models.CharField('Name', max_length=64)
    description = models.CharField('Description', max_length=2048)
    confirmation_message = models.CharField('Confirmation Message', max_length=2048)

    def to_json(self):
        """
        Returns json representing this client.
        """

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "confirmation_message": self.confirmation_message,
            }

    def __str__(self):    # pragma: nocover (mostly just for debugging)
        return self.name


class MessengerPhoneNumber(models.Model):

    app_label = 'messenger'

    messenger_client = models.ForeignKey(MessengerClient, on_delete=models.PROTECT)
    phone_number = models.CharField('Phone Number', max_length=10, db_index=True, unique=True)
    description = models.CharField('Description', max_length=512, blank=True, null=True)

    def __str__(self):    # pragma: nocover (mostly just for debugging)
        return str(self.messenger_client) + ' - ' + self.phone_number


class MessengerLocation(models.Model):

    app_label = 'messenger'

    LOCATION_CHOICES = [('DHSEM Evacuation Zone', 'DHSEM Evacuation Zone'), ('ZIP Code', 'ZIP Code')]

    location_type = models.CharField('Location Type', max_length=32, choices=LOCATION_CHOICES)
    value = models.CharField('Value', max_length=128)

    def __str__(self):    # pragma: nocover (mostly just for debugging)
        return self.location_type + " " + self.value


def get_locations_helper(notification=None):
    """
    Returns all locations for the given notification.  If notification
    is None, it returns all notifications available.
    """

    if notification:
        location_types = notification.locations.all().values('location_type').order_by('location_type')
    else:
        location_types = MessengerLocation.objects.all().values('location_type').order_by('location_type')

    response = {}

    # Add all our location types.
    for location_type in location_types:

        response[location_type['location_type']] = []

    # Add each location.
    for location in MessengerLocation.objects.all().order_by('location_type', 'value'):

        response[location.location_type].append(location.value)

    return response


class MessengerNotification(models.Model):

    app_label = 'messenger'

    FORMATTER_CHOICES = [('DHSEMFormatter', 'DHSEMFormatter'), ('ElectionFormatter', 'ElectionFormatter')]

    messenger_client = models.ForeignKey(MessengerClient, on_delete=models.PROTECT)
    locations = models.ManyToManyField(MessengerLocation)

    # REVIEW allow day to be null to indicate 'every day' ?
    # REVIEW allow day to be a full timestamp?
    day = models.DateField('Day on which notification should be sent')
    geo_layer_url = models.CharField('Geo Layer URL', max_length=1024, blank=True, null=True)
    formatter = models.CharField('Formatter class to render message', max_length=64, blank=True, null=True, choices=FORMATTER_CHOICES)

    def get_message_by_lang(self, lang):
        """
        Returns correct message for this notification, based on specified language preference.
        """

        messages = []

        # Give preference to message matching subscriber's lang preference, if any.
        if lang:
            messages = self.messengermessage_set.filter(lang=lang)

        # If no lang preference, if nothing matched lang preference, default to english.
        if not messages:
            messages = self.messengermessage_set.filter(lang='en')

        return messages.first() if messages else None

    def get_message(self, subscriber):
        """
        Returns correct message for this notification, based on subscriber's language preference.
        """

        return self.get_message_by_lang(lang=subscriber.lang)

    def to_json(self):
        """
        Returns json representing this notification.
        """

        data = {
            "id": self.id,
            "day": date_json(self.day),
            "geo_layer_url": self.geo_layer_url,
            "formatter": self.formatter,
            "messages": []
            }

        for message in self.messengermessage_set.all():

            data["messages"].append(message.to_json())

        data["locations"] = get_locations_helper(notification=self)

        return data

    def __str__(self):    # pragma: nocover (mostly just for debugging)
        return str(self.id) + ' - ' + str(self.messenger_client) + ' - ' + str(self.day)


# "https://services2.arcgis.com/qvkbeam7Wirps6zC/arcgis/rest/services/Elections_2019/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry=-82.9988157%2C+42.351591&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=false&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pjson&token="
# "https://services2.arcgis.com/qvkbeam7Wirps6zC/arcgis/rest/services/Elections_2019/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry={lng}%2C+{lat}&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=*&returnGeometry=false&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pjson&token="


class MessengerMessage(models.Model):

    app_label = 'messenger'

    messenger_notification = models.ForeignKey(MessengerNotification, on_delete=models.PROTECT)
    lang = models.CharField('Language', max_length=32, default='en')
    message = models.CharField('Message', max_length=2048)

    def to_json(self):
        """
        Returns json representing this message.
        """

        return {
            "id": self.id,
            "lang": self.lang,
            "message": self.message,
            }

    def __str__(self):    # pragma: nocover (mostly just for debugging)
        return str(self.messenger_notification) + ' - ' + self.lang + ' - ' + self.message


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
    lang = models.CharField('Preferred Language', max_length=32, blank=True, null=True)
    created_at = models.DateTimeField('Time of initial subscription', default=timezone.now())
    last_status_update = models.DateTimeField('Time of last status change', default=timezone.now())

    def save(self, *args, **kwargs):
        """
        Override Model.save() to update latitude / longitude based on subscriber's address, as
        well as created_at / last_status_update.
        """

        location, address = geocode_address(street_address=self.address)
        if address:

            self.latitude = round(location['location']['y'], 8)
            self.longitude = round(location['location']['x'], 8)

        self.last_status_update = timezone.now()

        # Call the "real" save() method in base class
        super().save(*args, **kwargs)

    def __str__(self):    # pragma: nocover (mostly just for debugging)
        return str(self.messenger_client) + ' - ' + self.phone_number + ' - ' + self.address
