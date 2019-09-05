import json
import random
import requests

from django.conf import settings
from rest_framework.exceptions import PermissionDenied

from twilio.request_validator import RequestValidator
from twilio.rest import Client
from slackclient import SlackClient


class MsgHandlerConfig():

    def __init__(self, account_sid, auth_token, phone_sender_list):

        self.account_sid = account_sid
        self.auth_token = auth_token
        self.phone_sender_list = phone_sender_list

def get_dpw_msg_handler():

    account_sid = settings.AUTO_LOADED_DATA["TWILIO_ACCOUNT_SID"]
    auth_token = settings.AUTO_LOADED_DATA['TWILIO_AUTH_TOKEN']
    phone_sender_list = settings.AUTO_LOADED_DATA['TWILIO_PHONE_SENDERS']

    return MsgHandler(config=MsgHandlerConfig(account_sid=account_sid, auth_token=auth_token, phone_sender_list=phone_sender_list))

def get_elections_msg_handler(phone_sender_list):

    # REVIEW TODO once elections has set up a twilio acct, add their account strings
    # REVIEW move these config classes and functions somewhere else?

    account_sid = settings.AUTO_LOADED_DATA["TWILIO_ACCOUNT_SID"]
    auth_token = settings.AUTO_LOADED_DATA['TWILIO_AUTH_TOKEN']

    return MsgHandler(config=MsgHandlerConfig(account_sid=account_sid, auth_token=auth_token, phone_sender_list=phone_sender_list))

def get_dhsem_msg_handler(phone_sender_list):

    # REVIEW TODO once DHSEM has set up a twilio acct, add their account strings
    # REVIEW move these config classes and functions somewhere else?

    account_sid = settings.AUTO_LOADED_DATA["TWILIO_ACCOUNT_SID"]
    auth_token = settings.AUTO_LOADED_DATA['TWILIO_AUTH_TOKEN']

    return MsgHandler(config=MsgHandlerConfig(account_sid=account_sid, auth_token=auth_token, phone_sender_list=phone_sender_list))

class MsgHandler():
    """
    Handles sending text messages via twilio.
    """

    DRY_RUN = settings.DEBUG or settings.DRY_RUN

    @staticmethod
    def get_phone_number_key(phone_number):
        return int(phone_number[-2:]) % 20

    def __init__(self, config):

        self.config = config
        self.phone_senders = {}

        for phone_sender in self.config.phone_sender_list:

            key = MsgHandler.get_phone_number_key(phone_sender)
            self.phone_senders[key] = phone_sender

    def get_phone_sender(self, dest_phone_number=None):
        """
        Return one of the available phone numbers, either randomly selected
        or selected based on a hash of the destination phone number, so that
        the destination will always receive messages from the same number.
        """

        phone_sender = None
        if dest_phone_number:

            key = MsgHandler.get_phone_number_key(dest_phone_number)
            phone_sender = self.phone_senders.get(key)

        if not phone_sender:

            PHONE_SENDERS = settings.AUTO_LOADED_DATA['TWILIO_PHONE_SENDERS']
            random.seed()
            index = random.randrange(len(PHONE_SENDERS))
            phone_sender = PHONE_SENDERS[index]

        return phone_sender

    def validate(self, request):
        """
        Make sure the call came from twilio and is valid.
        Raise an exception if it is not.
        """

        validator = RequestValidator(self.config.auth_token)

        # Validate the request using its URL, POST data,
        # and X-TWILIO-SIGNATURE header
        request_valid = validator.validate(
                request.build_absolute_uri(),
                request.data,
                request.META.get('HTTP_X_TWILIO_SIGNATURE', ''))

        if not request_valid:
            raise PermissionDenied('Request failed twilio validation check')

    @staticmethod
    def get_fone_number(request, key='From'):
        """
        Returns phone number of message sender.
        """

        number = request.data[key].replace('+', '')
        if number.startswith('1'):
            number = number[1:]

        return number

    @staticmethod
    def get_address(request):
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
        client = Client(self.config.account_sid, self.config.auth_token)
        if MsgHandler.DRY_RUN or dry_run_param:
            return False

        if not phone_sender:
            phone_sender = self.get_phone_sender(dest_phone_number=phone_number)

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


class SlackMsgHandler():

    DRY_RUN = settings.DEBUG or settings.DRY_RUN

    def __init__(self):

        self.client = SlackClient(settings.AUTO_LOADED_DATA["SLACK_API_TOKEN"])
        self.ts = None

    def send(self, message, channel="#z_twilio"):
        """
        Slack a message to the City of Detroit #zzz slack channel
        """

        if SlackMsgHandler.DRY_RUN:
            return False

        result = self.client.api_call("chat.postMessage", channel=channel, text=message, timeout=60)

        self.ts = result.get('ts', None)
        return result.get('ok', False)

    def comment(self, message, channel="#z_twilio"):

        if SlackMsgHandler.DRY_RUN or not self.ts:
            return False

        result = self.client.api_call(
            "chat.postMessage",
            channel=channel,
            text=message,
            thread_ts=self.ts,
            timeout=60
        )

        return result.get('ok', False)

    def send_admin_alert(self, message, dry_run_param = False):
        """
        Send admins an alert.
        """

        if MsgHandler.DRY_RUN or dry_run_param:
            return False    # pragma: no cover

        # REVIEW: use a better channel (e.g., #alerts-admin?)
        result = self.client.api_call("chat.postMessage", channel="#z_testing", text=message, timeout=60)

        self.ts = result.get('ts', None)
        return result.get('ok', False)
