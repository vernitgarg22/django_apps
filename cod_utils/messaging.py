import json
import random
import requests

from django.conf import settings

from twilio.request_validator import RequestValidator
from twilio.rest import Client


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

    def send_text(self, phone_number, text, dry_run_param = False):
        """
        Send a text message via twilio rest client
        """
        client = Client(MsgHandler.ACCOUNT_SID, MsgHandler.AUTH_TOKEN)
        if MsgHandler.DRY_RUN or dry_run_param:
            return False

        try:
            message = client.messages.create(
                to = "+1" + phone_number,
                from_ = MsgHandler.get_phone_sender(),
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
        if dry_run_param:    # pragma: no cover
            return False

        success = True

        for number in admin_numbers:
            try:
                message = client.messages.create(
                    to = "+1" + number,
                    from_ = MsgHandler.get_phone_sender(),
                    body = text,
                )
                if message.status == 'failed':    # pragma: no cover
                    success = FALSE
            except:    # pragma: no cover
                print("Error received sending twilio msg")
                return False

        return success


class SlackMsgHandler():

    WEBHOOK_URL = "https://hooks.slack.com/services/" + settings.AUTO_LOADED_DATA["SLACK_ZZZ_TOKEN"]
    DRY_RUN = settings.DEBUG or settings.DRY_RUN

    def send(self, message):
        """
        Slack a message to the City of Detroit #zzz slack channel
        """

        slack_data = { "text": message }
        if SlackMsgHandler.DRY_RUN:
            return False
        response = requests.post(
            SlackMsgHandler.WEBHOOK_URL, data=json.dumps(slack_data),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
            # Don't raise an error, at least for now, just keep running
            # raise ValueError(
            #     'Request to slack returned {}, the response is:\n{}'.format(response.status_code, response.text)
            # )
            return False
        else:
            return True


