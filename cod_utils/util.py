import datetime
import json
import random
import pytz
from pytz import timezone

from django.conf import settings
from django.core.exceptions import PermissionDenied

from twilio.util import RequestValidator
from twilio.rest import TwilioRestClient


def date_json(date):
    """
    Convert a datetime or date object to json string format
    """

    if not date:
        return ""

    dt = date
    if type(date) is datetime.date:
        dt = datetime.datetime(date.year, date.month, date.day)

    return dt.strftime("%Y-%m-%dT%H:%M:%S")

def get_local_time(now_utc = datetime.datetime.now(pytz.utc)):
    """
    Returns now_utc, converted to eastern standard time.
    """

    return now_utc.astimezone(timezone('US/Eastern'))

def tomorrow(today = datetime.date.today()):
    """
    Return tomorrow as a datetime object.  If today is passed
    in (as 'YYYYMMDD') the value returned will be a day
    later than the date represented by today
    """
    if type(today) == str:
        today = datetime.datetime.strptime(today, "%Y%m%d")

    return today + datetime.timedelta(days=1)


def get_week_start_end(date):
    """
    Return datetime date objects representing first and last date
    in the week that date belongs to
    """

    days = date.weekday()
    start = date if days == 0 else date - datetime.timedelta(days=days)
    end = date if days == 6 else date + datetime.timedelta(days=6-days)

    return start, end

def clean_list(values):
    """
    Returns a cleaned-up version of values which has
    any empty strings or strings with only white-space removed.
    Values with leading or trailing white-space will also have
    that white space removed.
    """

    dest = []
    while values:
        val = values.pop(0)
        if type(val) is str:
            val = val.strip()
        if val != '':
            dest.append(val)
    return dest


def split_csv(str):
    """
    Split comma-delimited value into list.
    Note:
    - Empty string or None results in empty list.
    - Individual empty strings do not add empty elements.
        e.g., 
            ',' -> []
            ',foo,bar' -> ['foo', 'bar']
    """

    if not str or str == ',':
        return []

    values = str.split(',')
    return clean_list(values)


def clean_comma_delimited_string(string):
    """
    Takes a comma-delimited string and makes sure it contains
    only unique values and begins and ends with commas.  If string
    is None or '' an empty string is returned
    """

    if string == None or string == '':
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
        client = TwilioRestClient(MsgHandler.ACCOUNT_SID, MsgHandler.AUTH_TOKEN)
        if MsgHandler.DRY_RUN or dry_run_param:
            return False
        else:
            client.messages.create(
                to = "+1" + phone_number,
                from_ = MsgHandler.get_phone_sender(),
                body = text,
            )
            return True
