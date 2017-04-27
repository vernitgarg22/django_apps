from operator import attrgetter
from itertools import chain
import copy
import datetime
import requests

from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import Http404

from .models import BiWeekType, ScheduleDetail
import cod_utils.util


def check_month_val(year, month, day):
    if not day:
        return False
    if year:
        if day.year != int(year):
            return False
    if month:
        if day.month != int(month):
            return False
    return True

def check_month(year, month, detail):
    if detail.detail_type == 'start-date' or detail.detail_type == 'end-date':
        return True
    return check_month_val(year, month, detail.normal_day) or check_month_val(year, month, detail.new_day)

def filter_month(year, month, details):
    return [ detail for detail in details if check_month(year, month, detail) ]

def get_day_of_week_diff(today, next_day):
    """
    Return number of days between 'today', where today is a datetime.date object,
    and the next instance of 'next_day', where next_day is the name of a day 
    of the week (e.g., 'monday')
    """

    today_val = today.weekday()
    next_day_val = ScheduleDetail.DAYS.index(next_day)

    diff = next_day_val - today_val
    if next_day_val < today_val:
        diff = diff + 7
    return diff

def get_next_pickup(today, next_day, week):
    """
    Figure out what day corresponds with next_day, given the
    particular alternating biweekly schedule designated by 'week'
    """

    diff  = get_day_of_week_diff(today, next_day)

    possible_date = today + datetime.timedelta(days = diff)

    if week in [ 'a', 'b' ] and not ScheduleDetail.check_date_service(possible_date, BiWeekType.from_str(week)):
        possible_date = possible_date + datetime.timedelta(days = 7)

    return possible_date

def add_route_pickup_info(route, service, today):

    week = '' if service == 'trash' else route['week']
    next_pickup = get_next_pickup(today=today, next_day=route['day'], week=week)
    route_dest = copy.copy(route)
    route_dest['next_pickup'] = cod_utils.util.date_json(next_pickup)
    return route_dest

def get_next_pickups(route_ids, schedule_details, today=datetime.date.today()):
    """
    """

    r = requests.get(ScheduleDetail.GIS_URL_ALL)
    routes = [ { "route": feature['attributes']['FID'], 'services': feature['attributes']['services'], 'day': feature['attributes']['day'], 'week': feature['attributes']['week'], 'contractor': feature['attributes']['contractor'] } for feature in r.json()['features'] if int(feature['attributes']['FID']) in route_ids ]
 
    content = {}

    # add next pickups for each route
    for route in routes:
        service = route.pop('services')
        if service == 'all':
            content[ScheduleDetail.TRASH] = add_route_pickup_info(route, ScheduleDetail.TRASH, today)
            content[ScheduleDetail.RECYCLING] = add_route_pickup_info(route, ScheduleDetail.RECYCLING, today)
            content[ScheduleDetail.BULK] = add_route_pickup_info(route, ScheduleDetail.BULK, today)
        else:
            next_pickup = get_next_pickup(today=today, next_day=route['day'], week=route['week'])
            route['next_pickup'] = cod_utils.util.date_json(next_pickup)
            content[service] = route

    return content


@api_view(['GET'])
def get_schedule_details(request, waste_area_ids=None, year=None, month=None, format=None):
    """
    List details to the waste collection schedule for a waste area
    """

    # Throw error if there is an unrecognized query param
    for param in request.query_params.keys():
        if param not in ['today']:
            return Response("Invalid param: " + param, status=status.HTTP_400_BAD_REQUEST)

    # Allow caller to specify what 'today' is
    today = request.query_params.get('today')
    if not today:
        today = datetime.date.today()

    if type(today) is str:
        today = datetime.date(int(today[0:4]), int(today[4:6]), int(today[6:8]))

    # get details that apply citywide
    citywide_details = ScheduleDetail.objects.filter(waste_area_ids__exact='')

    wa_ids = [ int(wa_id) for wa_id in waste_area_ids.split(',') ]

    wa_details = ScheduleDetail.objects.none()

    # get waste schedule details for each waste area requested
    for wa_id in wa_ids:
        wa_details = wa_details | ScheduleDetail.objects.filter(waste_area_ids__contains=wa_id)

    if month or year:
        citywide_details = filter_month(year, month, citywide_details)
        wa_details = filter_month(year, month, wa_details)

    # sort the different sets of results by 'normal_day'
    details = sorted(chain(citywide_details, wa_details), key=attrgetter('sort_value'))

    # get next pickup for each route
    next_pickups = get_next_pickups(wa_ids, details, today)

    # build an array of json objects, one for each detail
    content = { 'next_pickups': next_pickups, 'details': [detail.json() for detail in details] }

    return Response(content)
