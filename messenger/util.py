from messenger.models import MessengerClient, MessengerPhoneNumber, MessengerNotification, MessengerSubscriber

# from cod_utils import util
from cod_utils.messaging import MsgHandler


import pdb


def send_messages(today, dry_run_param, client_name):
    """
    Send out any and all notifications.
    """


    # TODO figure out what the return value should be


    pdb.set_trace()


    if not MessengerClient.objects.filter(name=client_name).exists():
        raise CommandError(f"Messenger Client '{client_name}' not found")

    client = MessengerClient.objects.get(name=client_name)

    # TODO: filter notification objects by client

    notifications = ElectionNotification.objects.filter(day=today)
    if not notifications:
        return

    subscribers = ElectionSubscriber.objects.all()
    for subscriber in subscribers:

        for notification in notifications:

            message = None

            if notification.notification_type == 'reminder':

                # TODO create a city-wide reminder - add in precinct info, etc.

                message = notification.message

            else:

                # TODO check if subscriber is geofenced by this notification
                # TODO if subscriber is geofenced here, then create the notification

            # Send the message?
            if message:
                MsgHandler().send_text(phone_number=subscriber.phone_number, phone_sender=elections_info_number, text=message)
