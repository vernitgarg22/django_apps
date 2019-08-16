import sys
from abc import ABC, abstractmethod
import requests
from urllib.parse import quote_plus

from messenger.models import MessengerClient, MessengerPhoneNumber, MessengerNotification, MessengerSubscriber

from cod_utils.messaging import MsgHandler
from cod_utils.util import date_json


class NotificationException(Exception):
    """Exception raised for errors while handling a notification

    Attributes:
        client_name -- name of the client that the notification belongs to
        message -- explanation of the error
    """

    def __init__(self, client_name, message):

        self.client_name = client_name
        self.message = message


class BaseNotificationFormatter(ABC):

    def __init__(self, notification, subscriber, geo_layer_data):

        self.notification = notification
        self.subscriber = subscriber
        self.geo_layer_data = geo_layer_data

    @abstractmethod
    def format_message(self):
        while False:
            yield None

class ElectionFormatter():

    def __init__(self, notification, subscriber, geo_layer_data):

        self.notification = notification
        self.subscriber = subscriber
        self.geo_layer_data = geo_layer_data

    def format_message(self):

        for feature in self.geo_layer_data["features"]:

            boundary = feature["attributes"]["boundary_t"]
            if boundary == "Election Precincts":

                precinct_location = feature["attributes"]["precinct_location"]
                precinct_name = feature["attributes"]["precinct_name"]
                pollxy = feature["attributes"]["pollxy"]
                comma_pos = pollxy.find(',')
                lat = pollxy[comma_pos + 1 : ]
                lng = pollxy[0 : comma_pos]

                return self.notification.message.format(location=precinct_location, name=precinct_name, url_safe_name=quote_plus(precinct_name), lat=lat, lng=lng)

        return self.notification.message

BaseNotificationFormatter.register(ElectionFormatter)


def format_message(notification, subscriber):
    """
    Creates a message for the given notification.
    """

    # If the notification has no geo layer, just use the notification's message as is.
    if not notification.geo_layer_url:
        return notification.message

    url = notification.geo_layer_url.format(lng=subscriber.longitude, lat=subscriber.latitude)
    response = requests.get(url)
    if not response.ok:
        raise NotificationException(client_name=notification.messenger_client.name, 
                message="Notification geo layer url not available")

    if not notification.formatter:
        raise NotificationException(client_name=notification.messenger_client.name, 
                message="Notification formatter not set")

    klz = getattr(sys.modules[__name__], notification.formatter)
    if not klz:
        raise NotificationException(client_name=notification.messenger_client.name, 
            message="Notification formatter {} not found".format(notification.formatter))

    formatter = klz(notification=notification, subscriber=subscriber, geo_layer_data=response.json())
    return formatter.format_message()


class MessagesMeta():

    class NotificationMeta():

        def __init__(self, notification_id, message, geo_layer_url, formatter, num_messages_sent):

            self.notification_id = notification_id
            self.message = message
            self.geo_layer_url = geo_layer_url
            self.formatter = formatter
            self.num_messages_sent = num_messages_sent

        def describe(self):

            description = """
id:                 {id}
message:            {message}
geo layer url:      {geo_layer_url}
formatter:          {formatter}
num messages sent:  {num_messages_sent}
""".format(id=self.notification_id, 
message=self.message, geo_layer_url=self.geo_layer_url, formatter=self.formatter, num_messages_sent=self.num_messages_sent)

            return description

    def __init__(self, client_name, day):

        self.client_name = client_name
        self.day = day
        self.notifications_meta = []

    def add_notification_meta(self, notification, num_messages_sent):

        notification_meta = MessagesMeta.NotificationMeta(notification_id=notification.id, message=notification.message,
            geo_layer_url=notification.geo_layer_url, formatter=notification.formatter, num_messages_sent=num_messages_sent)
        self.notifications_meta.append(notification_meta)

    def describe(self):

        description = """
client: {client_name}
day:    {day}

notifications:""".format(client_name=self.client_name, day=self.day)

        if self.notifications_meta:

            for notification_meta in self.notifications_meta:
                description += "\n" + notification_meta.describe()


        else:
            description += "  (No notifications sent)"

        return description


def send_messages(client_name, day, dry_run_param):
    """
    Send out any and all notifications.

    Return Value:  dict with info about number of messages sent
    """

    if not MessengerClient.objects.filter(name=client_name).exists():
        raise CommandError(f"Messenger Client '{client_name}' not found")

    client = MessengerClient.objects.get(name=client_name)

    # Filter notification objects by client and day
    notifications = client.messengernotification_set.filter(day=day)
    if not notifications:
        return

    message_counter = {}

    # Filter subscribers by client and status and send the notifications
    subscribers = client.messengersubscriber_set.filter(status='active')
    for subscriber in subscribers:

        for notification in notifications:

            message = format_message(notification=notification, subscriber=subscriber)

            # REVIEW find a way to specify correct set of sender phone #s
            MsgHandler().send_text(phone_number=subscriber.phone_number, text=message)

            message_counter[notification.id] = message_counter.get(notification.id, 0) + 1

    # Return metadata about notifications sent
    messages_meta = MessagesMeta(client_name=client_name, day=day)
    for notification in notifications:
        messages_meta.add_notification_meta(notification=notification, num_messages_sent=message_counter.get(notification.id, 0))

    return messages_meta
