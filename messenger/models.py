import re

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from cod_utils.util import is_address_valid, geocode_address, date_json
from cod_utils.messaging.msg_handler import MsgHandler


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

    TYPE_CHOICES = [('sender', 'Notificaton Sender'), ('text_signup', 'Text Signup')]

    messenger_client = models.ForeignKey(MessengerClient, on_delete=models.PROTECT)
    phone_number = models.CharField('Phone Number', max_length=10, db_index=True, unique=True)
    description = models.CharField('Description', max_length=512, blank=True, null=True)
    number_type = models.CharField('Number Type', max_length=32, choices=TYPE_CHOICES, default='sender')

    def __str__(self):    # pragma: nocover (mostly just for debugging)
        return str(self.messenger_client) + ' - ' + self.phone_number


class MessengerLocation(models.Model):

    app_label = 'messenger'

    LOCATION_CHOICES = [('DHSEM Evacuation Zone', 'DHSEM Evacuation Zone'), ('ZIP Code', 'ZIP Code'), ('Citywide', 'Citywide')]
    PREFIX_CHOICES = [('dhsem_evac_zone', 'dhsem_evac_zone'), ('zipcode', 'zipcode'), ('citywide', 'citywide')]

    location_type = models.CharField('Location Type', max_length=32, choices=LOCATION_CHOICES)
    prefix = models.CharField('Prefix', max_length=16, default='citywide', choices=PREFIX_CHOICES)
    value = models.CharField('Value', max_length=128)

    def to_json(self):
        """
        Returns json representing this location.
        """

        return {
            "location_type": self.location_type,
            "prefix": self.prefix,
            "value": self.value,
        }

    def __str__(self):    # pragma: nocover (mostly just for debugging)
        return self.prefix + " " + self.value


def get_locations_helper(notification=None):
    """
    Returns all locations for the given notification.  If notification
    is None, it returns all notifications available.
    """

    if notification:
        location_types = notification.locations.all().values('location_type', 'prefix').order_by('location_type')
    else:
        location_types = MessengerLocation.objects.all().values('location_type', 'prefix').order_by('location_type')

    response = {}

    # Add all our location types.
    for location_type in location_types:

        response[location_type['prefix']] = {
            "description": location_type['location_type'],
            "values": []
        }

    if notification:
        locations = notification.locations.all().order_by('prefix', 'value')
    else:
        locations = MessengerLocation.objects.all().order_by('prefix', 'value')

    # Add each location.
    for location in locations:

        response[location.prefix]["values"].append(location.value)

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

    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive')]
    LANG_CHOICES = [('ar', 'Arabic'), ('bn', 'Bengali'), ('en', 'English'), ('es', 'Spanish'), ('default', 'Default (English)')]

    messenger_clients = models.ManyToManyField(MessengerClient)
    phone_number = models.CharField('Subscriber phone number', unique=True, max_length=32)
    status = models.CharField('Subscriber status', max_length=32, choices=STATUS_CHOICES, default='inactive')
    address = models.CharField('Home address', max_length=128)
    latitude = models.CharField('Latitude', max_length=32)
    longitude = models.CharField('Longitude', max_length=32)
    lang = models.CharField('Preferred Language', max_length=32, choices=LANG_CHOICES, default='default')
    created_at = models.DateTimeField('Time of initial subscription', default=timezone.now())
    last_status_update = models.DateTimeField('Time of last status change', default=timezone.now())


    def update_subscriber(self, **kwargs):
        """
        Update attributes of the subscriber.
        """

        changed = False
        for attribute in [ "status", "address", "latitude", "longitude", "lang" ]:

            value = kwargs.get(attribute, None)
            if value:
                setattr(self, attribute, value)
                changed = True

        if changed:
            self.save()

        return self

    @staticmethod
    def init_subscriber(phone_number, client, **kwargs):
        """
        Gets or creates a subscriber and initializes the subscriber's attributes.
        """

        subscriber, _ = MessengerSubscriber.objects.get_or_create(defaults=kwargs, phone_number=phone_number)

        subscriber.update_subscriber(**kwargs)

        # Add our client to the subscriber?
        if not subscriber.messenger_clients.filter(id=client.id).exists():
            subscriber.messenger_clients.add(client)

        return subscriber

    def change_status(self, activate):
        """
        Internal use only:  changes status to active or inactive and
        updates last_status_update to current time.
        """

        return self.update_subscriber(status="active" if activate else "inactive")

    def validate(self):
        """
        Throws an ValidationError exception if the subscriber's state is not valid.
        """

        if not re.fullmatch(r'\d{10}', self.phone_number):
            raise ValidationError({'phone_number': "Phone number must be 10 digits"})

        valid_statuses = [ status[0] for status in MessengerSubscriber.STATUS_CHOICES ]
        if self.status not in valid_statuses:
            raise ValidationError({'status': "Valid status values are {}".format(valid_statuses)})

        if not is_address_valid(street_address=self.address):
            raise ValidationError({'address': "Address '{}'' is not specific enough".format(self.address)})

        if not (self.latitude and self.longitude):
            raise ValidationError({'address': "Address '{}'' did not map to a latitude or longitude".format(self.address)})

        valid_languages = [ choice[0] for choice in MessengerSubscriber.LANG_CHOICES ]
        if self.lang not in valid_languages:
            raise ValidationError({'lang': "Valid languages are {}".format(valid_languages)})

        if not (self.created_at and self.last_status_update) or self.created_at > self.last_status_update:
            raise ValidationError({'created_at': "Subscriber timestamps do not appear valid"})

    def save(self, *args, **kwargs):
        """
        Override Model.save() to update latitude / longitude based on subscriber's address, as
        well as created_at / last_status_update.
        """

        self.phone_number = MsgHandler.clean_fone_number(phone_number=self.phone_number)

        if not self.latitude or self.longitude:

            location, address = geocode_address(street_address=self.address)
            if not location:
                raise ValidationError({'address': "Address '{}' could not be located".format(self.address)})

            self.latitude = round(location['location']['y'], 8)
            self.longitude = round(location['location']['x'], 8)

        self.last_status_update = timezone.now()

        # Validate the subscriber
        self.validate()

        # Call the "real" save() method in base class
        super().save(*args, **kwargs)

    def __str__(self):    # pragma: nocover (mostly just for debugging)
        return self.phone_number + ' - ' + self.address
