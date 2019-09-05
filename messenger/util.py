import sys
from abc import ABC, abstractmethod
import requests
from urllib.parse import quote_plus

from django.core.management.base import CommandError

from messenger.models import MessengerClient, MessengerPhoneNumber, MessengerNotification, MessengerSubscriber

from cod_utils.messaging import MsgHandler, get_dhsem_msg_handler, get_elections_msg_handler
from cod_utils.util import date_json


def get_messenger_msg_handler(client):
    """
    Returns the msg handler for this client.
    """

    phone_sender_list = [ phone_number.phone_number for phone_number in client.messengerphonenumber_set.all() ]

    if client.name == 'Elections':

        return get_elections_msg_handler(phone_sender_list=phone_sender_list)

    elif client.name == 'DHSEM':

        return get_dhsem_msg_handler(phone_sender_list=phone_sender_list)

    else:  # pragma: nocover (should never get here)

        raise NotificationException(client_name=client.name, message="Msg handler for client '{}' not available".format(client.name))


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
        self.message = notification.get_message(subscriber)

    @abstractmethod
    def format_message(self):
        pass    # pragma: nocover (abstract method never gets called)

class ElectionFormatter(BaseNotificationFormatter):

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

                return self.message.message.format(location=precinct_location, name=precinct_name, url_safe_name=quote_plus(precinct_name), lat=lat, lng=lng)

        # Subscriber is not inside area affected by the notification: send no message
        return None

BaseNotificationFormatter.register(ElectionFormatter)

class DHSEMFormatter(ElectionFormatter):

    # REVIEW:  Make this unique when we know what the geo layer looks like

    pass    # pragma: nocover

BaseNotificationFormatter.register(DHSEMFormatter)


def format_message(notification, subscriber):
    """
    Creates a message for the given notification.
    """

    # Make sure a message is available.
    message = notification.get_message(subscriber)
    if not message:
        raise NotificationException(client_name=notification.messenger_client.name,
            message="Notification {id} has no message available for lang {lang}".format(id=notification.id, lang=subscriber.lang))

    # If the notification has no geo layer, just use the notification's message as is.
    if not notification.geo_layer_url:
        return message.message

    url = notification.geo_layer_url.format(lng=subscriber.longitude, lat=subscriber.latitude)
    response = requests.get(url, timeout=60)
    if not response.ok:
        raise NotificationException(client_name=notification.messenger_client.name,
                message="Notification geo layer url not available")

    if not notification.formatter:
        raise NotificationException(client_name=notification.messenger_client.name,
                message="Notification formatter not set")

    klz = getattr(sys.modules[__name__], notification.formatter, None)
    if not klz:
        raise NotificationException(client_name=notification.messenger_client.name,
            message="Notification formatter {} not found".format(notification.formatter))

    formatter = klz(notification=notification, subscriber=subscriber, geo_layer_data=response.json())
    return formatter.format_message()


class MessagesMeta():

    class NotificationMeta():

        def __init__(self, notification):

            self.notification = notification
            self.num_messages_sent = 0

        def update(self):

            self.num_messages_sent += 1

        def describe(self):

            messenger_message = self.notification.get_message_by_lang(lang=None)

            description = """
id:                 {id}
message:            {message}
geo layer url:      {geo_layer_url}
formatter:          {formatter}
num messages sent:  {num_messages_sent}
""".format(id=self.notification.id,
message=messenger_message.message, geo_layer_url=self.notification.geo_layer_url, formatter=self.notification.formatter, num_messages_sent=self.num_messages_sent)

            return description

    def __init__(self, client_name, day):

        self.client_name = client_name
        self.day = day
        self.notifications_meta = {}

    def update(self, notification):
        """
        Updates the notification metadata for each message sent.
        """

        if not self.notifications_meta.get(notification.id, None):

            notification_meta = MessagesMeta.NotificationMeta(notification=notification)
            self.notifications_meta[notification.id] = notification_meta

        self.notifications_meta[notification.id].update()

    def describe(self):

        description = """
client: {client_name}
day:    {day}

notifications:""".format(client_name=self.client_name, day=self.day)

        if self.notifications_meta:

            for notification_meta in self.notifications_meta.values():
                description += "\n" + notification_meta.describe()


        else:
            description += "  (No notifications sent)"

        return description


def send_messages(client_name, day, dry_run_param=False):
    """
    Send out any and all notifications.

    Return Value:  dict with info about number of messages sent
    """

    if not MessengerClient.objects.filter(name=client_name).exists():
        raise CommandError("Messenger Client '{client_name}' not found".format(client_name=client_name))

    client = MessengerClient.objects.get(name=client_name)

    msg_handler = get_messenger_msg_handler(client)
    messages_meta = MessagesMeta(client_name=client_name, day=day)

    # Filter notification objects by client and day
    notifications = client.messengernotification_set.filter(day=day)
    if not notifications:
        return messages_meta

    # Filter subscribers by client and status and send the notifications
    subscribers = client.messengersubscriber_set.filter(status='active')
    for subscriber in subscribers:

        for notification in notifications:

            message = format_message(notification=notification, subscriber=subscriber)
            if message:

                msg_handler.send_text(phone_number=subscriber.phone_number, text=message)

                messages_meta.update(notification=notification)

    return messages_meta
