import json
import random
import requests

from django.conf import settings
from rest_framework.exceptions import PermissionDenied

from twilio.request_validator import RequestValidator
from twilio.rest import Client
from slackclient import SlackClient


class MsgHandler():
    """
    Validates requests received from twilio
    """

    ACCOUNT_SID = settings.AUTO_LOADED_DATA["TWILIO_ACCOUNT_SID"]
    AUTH_TOKEN = settings.AUTO_LOADED_DATA['TWILIO_AUTH_TOKEN']
    DRY_RUN = settings.DEBUG or settings.DRY_RUN

    @staticmethod
    def get_phone_sender():
        """
        Return one of the available phone numbers, randomly selected
        """
        PHONE_SENDERS = settings.AUTO_LOADED_DATA['TWILIO_PHONE_SENDERS']
        random.seed()
        index = random.randrange(len(PHONE_SENDERS))
        return PHONE_SENDERS[index]

    def validate(self, request):   # pragma: no cover
        """
        Make sure the call came from twilio and is valid.
        Raise an exception if it is not.
        """

        AUTH_TOKEN = settings.AUTO_LOADED_DATA['TWILIO_AUTH_TOKEN']

        validator = RequestValidator(AUTH_TOKEN)

        # Validate the request using its URL, POST data,
        # and X-TWILIO-SIGNATURE header
        request_valid = validator.validate(
                request.build_absolute_uri(),
                request.data,
                request.META.get('HTTP_X_TWILIO_SIGNATURE', ''))

        if not request_valid:
            raise PermissionDenied('Request failed twilio validation check')

    def get_fone_number(self, request, key='From'):
        """
        Returns phone number of message sender.
        """

        number = request.data[key].replace('+', '')
        if number.startswith('1'):
            number = number[1:]

        return number

    def get_address(self, request):
        """
        Returns address of message sender.
        """

        address = request.data.get('Body', '').upper().strip()

        pos = address.find("DETROIT")
        if pos >= 0:
            address = address[0 : pos]

        return address


    def send_text(self, phone_number, text, phone_sender=None, dry_run_param=False):
        """
        Send a text message via twilio rest client
        """
        client = Client(MsgHandler.ACCOUNT_SID, MsgHandler.AUTH_TOKEN)
        if MsgHandler.DRY_RUN or dry_run_param:
            return False

        if not phone_sender:
            phone_sender = MsgHandler.get_phone_sender()

        try:
            message = client.messages.create(
                to = "+1" + phone_number,
                from_ = phone_sender,
                body = text,
            )
            return message.status != 'failed'
        except:    # pragma: no cover
            print("Error received sending twilio msg to number {}".format(phone_number))
            return False

    def send_admin_alert(self, text, dry_run_param = False):
        """
        Alert admins via twilio rest client
        """

        admin_numbers = settings.AUTO_LOADED_DATA['ADMIN_PHONE_NUMBERS']

        client = Client(MsgHandler.ACCOUNT_SID, MsgHandler.AUTH_TOKEN)
        if MsgHandler.DRY_RUN or dry_run_param:
            return False    # pragma: no cover

        success = True

        for number in admin_numbers:
            try:
                message = client.messages.create(
                    to = "+1" + number,
                    from_ = MsgHandler.get_phone_sender(),
                    body = text,
                )
                if message.status == 'failed':
                    success = FALSE    # pragma: no cover
            except:    # pragma: no cover
                print("Error received sending twilio msg")
                return False

        return success


class SlackMsgHandler():

    DRY_RUN = settings.DEBUG or settings.DRY_RUN

    def __init__(self):

        self.ts = None

    def send(self, message, channel="#z_twilio"):
        """
        Slack a message to the City of Detroit #zzz slack channel
        """

        if SlackMsgHandler.DRY_RUN:
            return False

        client = SlackClient(settings.AUTO_LOADED_DATA["SLACK_API_TOKEN"])
        result = client.api_call(
            "chat.postMessage",
            channel=channel,
            text=message,
            timeout=60
        )

        self.ts = result.get('ts', None)
        return result.get('ok', False)

    def comment(self, message, channel="#z_twilio"):

        if SlackMsgHandler.DRY_RUN or not self.ts:
            return False

        client = SlackClient(settings.AUTO_LOADED_DATA["SLACK_API_TOKEN"])
        result = client.api_call(
            "chat.postMessage",
            channel=channel,
            text=message,
            thread_ts=self.ts,
            timeout=60
        )

        return result.get('ok', False)
