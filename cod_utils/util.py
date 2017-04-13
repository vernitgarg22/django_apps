from django.conf import settings
from django.core.exceptions import PermissionDenied

from twilio.util import RequestValidator

# { "From": "9178428901", "Body": "ADD ME" }



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


class MsgValidator():
    """
    Validates requests received from twilio
    """

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
                request.path_info,
                request.data,
                request.META.get('X-TWILIO-SIGNATURE', ''))

        if not request_valid:
            raise PermissionDenied('Request failed twilio validation check')
