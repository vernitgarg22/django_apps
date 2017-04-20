from cod_utils.util import MsgHandler

from twilio.rest import TwilioRestClient


def no_validate(self, request):
    pass

MsgHandler.validate = no_validate
