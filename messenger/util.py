import sys
from abc import ABC, abstractmethod
import requests
from urllib.parse import quote_plus

from messenger.models import MessengerClient, MessengerPhoneNumber, MessengerNotification, MessengerSubscriber

from cod_utils.messaging import MsgHandler


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


def send_messages(client_name, day, dry_run_param):
    """
    Send out any and all notifications.
    """


    # TODO figure out what the return value should be


    if not MessengerClient.objects.filter(name=client_name).exists():
        raise CommandError(f"Messenger Client '{client_name}' not found")

    client = MessengerClient.objects.get(name=client_name)

    # Filter notification objects by client and day
    notifications = client.messengernotification_set.filter(day=day)
    if not notifications:
        return

    # Filter subscribers by client and status
    subscribers = client.messengersubscriber_set.filter(status='active')
    for subscriber in subscribers:

        for notification in notifications:

            message = format_message(notification=notification, subscriber=subscriber)
            MsgHandler().send_text(phone_number=subscriber.phone_number, text=message)
