import datetime
import json
import pytz
from pytz import timezone

from django.conf import settings
from django.core.exceptions import PermissionDenied


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

def get_local_time(now_utc = None):
    """
    Returns now_utc, converted to eastern standard time.
    """

    if not now_utc:
        now_utc = datetime.datetime.now(pytz.utc)
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
