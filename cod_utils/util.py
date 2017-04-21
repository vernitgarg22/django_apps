import datetime
import random

from django.conf import settings
from django.core.exceptions import PermissionDenied

from twilio.util import RequestValidator
from twilio.rest import TwilioRestClient


def tomorrow():
    """
    Return tomorrow as a datetime object
    """
    return datetime.date.today() + datetime.timedelta(days=1)


def clean_comma_delimited_string(string):
    """
    Takes a comma-delimited string and makes sure it contains
    only unique values and begins and ends with commas.  If string
    is None return empty string
    """

    if string == None:
        return ''

    tmp = [ str(val) + ',' for val in sorted(set(string.split(','))) if val ]
    return ',' + ''.join(tmp)


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

    def validate(self, request):
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

    def send_text(self, phone_number, text, dry_run_param = False):
        """
        Send a text message via twilio rest client
        """
        client = TwilioRestClient(MsgHandler.ACCOUNT_SID, MsgHandler.AUTH_TOKEN)
        if not MsgHandler.DRY_RUN and not dry_run_param:
            client.messages.create(
                to = "+1" + phone_number,
                from_ = MsgHandler.get_phone_sender(),
                body = text,
            )
