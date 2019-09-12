import datetime
import json
import pytz
from pytz import timezone
import re

from django.conf import settings
from django.utils import timezone

from arcgis import gis, geocoding


def date_json(date, **options):
    """
    Convert a datetime or date object to json string format
    """

    if not date:
        return ""

    dt = date
    if type(date) is datetime.date:
        dt = datetime.datetime(date.year, date.month, date.day)

    dt_str = dt.strftime("%Y-%m-%dT%H:%M:%S.000")
    tzinfo = options.get("add_tz", "Z")
    if tzinfo:
        dt_str += tzinfo
    return dt_str

def get_local_time(now_utc = None):
    """
    Returns now_utc, converted to eastern standard time.
    """

    if not now_utc:
        # TODO timezone.localtime() ignores DST
        return timezone.localtime()
    return now_utc.astimezone()

def tomorrow(today = datetime.date.today()):
    """
    Return tomorrow as a datetime object.  If today is passed
    in (as 'YYYYMMDD') the value returned will be a day
    later than the date represented by today
    """
    if type(today) == str:
        today = datetime.datetime.strptime(today, "%Y%m%d")

    return today + datetime.timedelta(days=1)


# TODO: alter this to return a range, beginning at the beginning of whatever
# week 'date' is in and ending N days from 'date'
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


def get_parcel_id(path, offset):
    """
    Parse out a parcel id from the path and return it. (This is necessary because a 
    lot of parcel ids contain a dot, and urls with dots are problematic in django
    because it treats them as format delimiters - e.g., "http://<host>/path.json")
    """

    parcel_id = path.split('/')[offset]

    # Some callers replace '.' with '_'
    return parcel_id.replace('_', '.')

def is_address_valid(street_address):
    """
    Returns True if street_address appears to be valid.
    """

    return re.search(r'\d\s\w', street_address)

    # if street_address == 'detroit' or re.fullmatch('[0-9]*', street_address):
    #     return None, None


class GISLocation():

    def __init__(self, latitude, longitude, address):

        self.latitude = round(latitude, 8)
        self.longitude = round(longitude, 8)
        self.address = address


def geocode_address(street_address):
    """
    Returns geocoded location and address object if address can be geocoded
    with enough accuracy. Otherwise, returns None.
    """

    street_address = street_address.strip().lower()

    # Verify address is not just 'detroit' or a zip code, because those are not
    # specific enough.
    if not is_address_valid(street_address=street_address):
        return None

    # Setup arcgis environment
    AGO_USER = settings.AUTO_LOADED_DATA["AGO_USER"]
    AGO_PASS = settings.AUTO_LOADED_DATA["AGO_PASS"]
    ago = gis.GIS(url="https://detroitmi.maps.arcgis.com", username=AGO_USER, password=AGO_PASS)

    geocoder = geocoding.get_geocoders(ago)[0]

    # Geocode the address
    geocode_result = geocoding.geocode(address=street_address, as_featureset=True, out_sr=4326, geocoder=geocoder)
    features = geocode_result.features

    # No results found?
    if not features or features[0].get_value("Score") < 50:
        return None

    # Return location information.
    return GISLocation(latitude=features[0].get_value("geometry")["y"], longitude=features[0].get_value("geometry")["x"],
        address=features[0].get_value("Match_addr"))
