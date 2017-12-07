import datetime
import requests

from waste_schedule.models import ScheduleDetail, BiWeekType
import cod_utils.util


class WeekRouteInfo():

    WEEK_MAP = {
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5,
        'sunday': 6,
    }

    def __init__(self, date):

        # initialize the array of days, each containing an empty dict
        self.data = [ {} for day in WeekRouteInfo.WEEK_MAP.values() ]

        # what kind of week are we in?  ('A' or 'B'?)
        self.week_type = ScheduleDetail.get_date_week_type(date)

    def add_day_route(self, route):
        """
        Adds information for a particular route, for a particular day.
        """

        index = WeekRouteInfo.WEEK_MAP[route.pop('day')]

        week_type = route.get('week')
        if week_type == ' ' or week_type.lower() == str(self.week_type).lower() or route['services'] == ScheduleDetail.ALL:
            self.data[index][route.pop('FID')] = route

    def reschedule_service(self, old_date, new_date, service_type):
        """
        Reschedules the particular type of service from old_day to
        new_day.  Note: if service_type is 'all', then all services
        get rescheduled.
        """

        self.data.pop()
        self.data.insert(old_date.weekday(), {})

    def get_day(self, date):
        """
        Returns all route info for the particular day
        """
        return self.data[date.weekday()]


class ScheduleDetailMgr():

    # the one and only singlton instance of the ScheduleDetailMgr
    __instance = None

    def __init__(self):
        # Make sure only 1 instance of ScheduleDetailMgr is created
        if ScheduleDetailMgr.__instance:
            raise Exception("call ScheduleDetailMgr.instance() to get access to ScheduleDetailMgr")

    def instance():
        """
        Should return one-and-only instance of this class.
        """
        if ScheduleDetailMgr.__instance is None:
            ScheduleDetailMgr.__instance = ScheduleDetailMgr()
        return ScheduleDetailMgr.__instance

    def get_service_start_and_end(self, service):
        """
        Returns the ScheduleDetail objects that indicate when the given
        service starts and ends.
        """
        details = ScheduleDetail.objects.filter(service_type='yard waste')
        start = details.filter(detail_type='start-date')
        end = details.filter(detail_type='end-date')
        if start and end:
            return start[0], end[0]
        else:
            return None, None

    def is_service_active(self, service, date):
        """
        Return True if the given service is active on the given date.  If the service
        is not year-round, and does not have start-date and end-dates set up, then
        return False.  If the service is year-round, then return True.
        """
        if type(date) is datetime.datetime:
            date = date.date()
        if service in ScheduleDetail.YEAR_ROUND_SERVICES:
            return True
        start, end = self.get_service_start_and_end(service)
        if start and end:
            return date >= start.new_day and date <= end.new_day
        else:
            return False


    #
    # Here's the new idea I am trying out with get_routes_for_date:
    #
    # 1.  Call get_routes_for_date with whatever tomorrow's date is
    #
    # 2.  get_routes_for_date returns all routes that will be getting
    #     pickups on that date.  Any routes that normally would be
    #     getting pickups on that date but instead are getting delayed
    #     due to a schedule change (e.g., holiday) will not be returned.
    #
    # 3.  Caller should loop through all those routes and figure out
    #     who is subscribed to each route and send out notifications
    #     accordingly
    #
    #     Note:  in order for get_routes_for_date() to do this it will 
    #            need to:
    #
    #     1.  create array of days representing each day of the week
    #         that the current day belongs to
    #     2.  loop through each day of week, adding routes to each
    #         day that *normally* get pickups on that day
    #     3.  now check schedule changes for each day, in order:  any
    #         citywide schedule change should delay pickups for routes
    #         in any subsequent days for the week back by one day
    #

    def get_schedule_details(self, date):
        """
        Returns all schedule details with new day or normal day matching the given date
        """

        changes = ScheduleDetail.objects.filter(detail_type__in=['info', 'schedule']).filter(normal_day__exact=date)

        start_end_range_query = ScheduleDetail.objects.filter(detail_type__in=['start-date', 'end-date'])

        start_end_ranges = start_end_range_query.filter(normal_day__exact=date) | start_end_range_query.filter(new_day__exact=date)

        return changes | start_end_ranges

    def get_citywide_schedule_changes(self, date):
        """
        Returns schedule details that are city-wide (i.e., not tied to a specific route) and match given date
        """

        details = ScheduleDetail.objects.filter(detail_type__exact='schedule')
        details = details.filter(waste_area_ids__isnull=True) | details.filter(waste_area_ids__exact='')
        return details.filter(normal_day__exact=date)

    # TODO refactor the 'route info' stuff into its own class

    def get_route_info(self, route_id):
        """
        Returns info about the particular route
        """

        # TODO cache this

        # get the data from gis server
        r = requests.get(ScheduleDetail.GIS_URL_ALL)

        # find the correct route info and return it
        for feature in r.json()['features']:
            if int(feature['attributes']['FID']) == int(route_id):
                return feature['attributes']

        return {}      # pragma: no cover (should never get here)


    def get_regular_week_routes(self, date):
        """
        Return array of route information for each day of the week - each
        element in the array represents a day of the week, starting with 
        with monday and ending with sunday.
        """

        # initialize the array of days, each containing an empty dict
        week_route_info = WeekRouteInfo(date)

        # get the data from gis server
        r = requests.get(ScheduleDetail.GIS_URL_ALL)

        # put each piece of route info, into the correct day
        for feature in r.json()['features']:
            week_route_info.add_day_route(feature['attributes'])

        return week_route_info

    # TODO: alter this to return a range, beginning at the beginning of whatever
    # week 'date' is in and ending N days from 'date'
    def get_week_schedule_changes(self, date):
        """
        Return schedule changes for the week that date belongs to.
        """

        schedule_changes = {}
        start_date, end_date = cod_utils.util.get_week_start_end(date)
        while start_date <= end_date:
            changes_tmp = self.get_citywide_schedule_changes(start_date)
            schedule_changes[start_date.strftime("%Y%m%d")] = changes_tmp
            start_date = start_date + datetime.timedelta(days=1)

        # TODO add in schedule changes that are not city-wide

        return schedule_changes

    def get_week_routes(self, date):
        """
        Return array of route information for each day in the week that
        date belongs to - each element in the array represents a day
        of the week, starting with with monday and ending with sunday.
        Any pickups on or after a schedule change (e.g., a holiday
        get pushed back by one day.
        """

        week_route_info = self.get_regular_week_routes(date)

        week_schedule_changes = self.get_week_schedule_changes(date)

        start_date, end_date = cod_utils.util.get_week_start_end(date)
        while start_date <= end_date:

            schedule_changes = week_schedule_changes.get(start_date.strftime("%Y%m%d"))

            if schedule_changes:

                for change in schedule_changes:
                    week_route_info.reschedule_service(change.normal_day, change.new_day, change.service_type)

            start_date = start_date + datetime.timedelta(days=1)

        return week_route_info

    def get_day_routes(self, date):
        """
        Return dict of routes that operate on the given date.  If the date
        happens to be a holiday (or any other kind of schedule change) then
        the routes effected by the schedule change will not be returned.
        """

        week_route_info = self.get_week_routes(date)
        return week_route_info.get_day(date)

    def check_all_service_week(self, date, route):
        """
        Returns 'trash' if that is the only service getting picked up
        on the given week, otherwise returns all
        """

        if route['services'] != ScheduleDetail.ALL:
            return route['services']     # pragma: no cover (should never get here)

        week = route['week']
        if ScheduleDetail.check_date_service(date, BiWeekType.from_str(week)):
            return ScheduleDetail.ALL
        else:
            return ScheduleDetail.TRASH
