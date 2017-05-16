import datetime
import requests

from django.test import Client
from django.test import TestCase

from django.core.exceptions import ValidationError

import cod_utils.util
import tests.disabled

from waste_schedule.models import ScheduleDetail
from waste_schedule.schedule_detail_mgr import ScheduleDetailMgr, WeekRouteInfo

from waste_schedule import util
import waste_schedule.views


# TODO put this in a util.py file
def cleanup_model(model):
    model.objects.all().delete()

def cleanup_db():
    cleanup_model(ScheduleDetail)

def make_schedule_detail(detail_type='schedule', service_type='trash', normal_day=None, new_day=None):
    detail = ScheduleDetail(detail_type=detail_type, service_type=service_type, normal_day=normal_day, new_day=new_day)
    detail.clean()
    detail.save()
    return detail


class WasteScheduleInitTests(TestCase):

    def setUp(self):
        cleanup_db()
        self.maxDiff = None

    def test_check_month_val(self):
        self.assertTrue(util.check_month_val(2017, 7, datetime.date(2017, 7, 30)), "Date belongs to given month and year")

    def test_check_month_val_none(self):
        self.assertFalse(util.check_month_val(2017, 7, None), "Null date does not match")

    def test_check_month_val_month(self):
        self.assertFalse(util.check_month_val(2017, 8, datetime.date(2017, 7, 30)), "Date does not belong to given month")

    def test_check_month_val_year(self):
        self.assertFalse(util.check_month_val(2016, 7, datetime.date(2017, 7, 30)), "Date does not belong to given year")

    def test_check_month(self):
        detail = make_schedule_detail(detail_type='schedule', service_type=ScheduleDetail.RECYCLING, normal_day=datetime.date(2017, 7, 30), new_day=datetime.date(2017, 7, 31))
        self.assertTrue(util.check_month(2017, 7, detail), "check_month() matches Schedule Detail to month and year")

    def test_check_month_start_date(self):
        detail = make_schedule_detail(detail_type='start-date', service_type=ScheduleDetail.RECYCLING, normal_day=datetime.date(2017, 7, 30), new_day=datetime.date(2017, 7, 31))
        self.assertTrue(util.check_month(2017, 1, detail), "check_month() matches start date Schedule Detail")

    def test_filter_month(self):
        detail = make_schedule_detail(detail_type='schedule', service_type=ScheduleDetail.RECYCLING, normal_day=datetime.date(2017, 7, 30), new_day=datetime.date(2017, 7, 31))
        self.assertTrue(util.filter_month(2017, 7, [detail]) == [detail], "filter_month() returns list of details belonging to month and year")

    def test_filter_month_start_date(self):
        detail = make_schedule_detail(detail_type='start-date', service_type=ScheduleDetail.RECYCLING, normal_day=datetime.date(2017, 7, 30), new_day=datetime.date(2017, 7, 31))
        self.assertTrue(util.filter_month(2017, 1, [detail]) == [detail], "filter_month() returns list of details including start date details")

    def test_get_day_of_week_diff1(self):
        self.assertTrue(util.get_day_of_week_diff(datetime.date(2017, 4, 28), 'monday') == 3, "get_day_of_week_diff() returns 3 days between friday and monday")

    def test_get_day_of_week_diff2(self):
        self.assertTrue(util.get_day_of_week_diff(datetime.date(2017, 4, 28), 'friday') == 0, "get_day_of_week_diff() returns no days between friday and friday")

    def test_get_day_of_week_diff3(self):
        self.assertTrue(util.get_day_of_week_diff(datetime.date(2017, 4, 27), 'friday') == 1, "get_day_of_week_diff() returns 1 day between thursday and friday")

    def test_biweektype_from_str(self):
        self.assertTrue(util.BiWeekType.from_str('a') == util.BiWeekType.A)

    def test_biweektype_from_str_error(self):
        with self.assertRaises(Exception, msg="Invalid week types raises an error") as error:
            util.BiWeekType.from_str(' ')


# TODO organize tests better - maybe put related tests into subdirectories under /tests ?
class WeekRouteInfoTests(TestCase):

    def setUp(self):
        """
        Set up each unit test, including making sure database is properly cleaned up before each test
        """
        cleanup_db()

    def test_add_day_route(self):

        monday = datetime.datetime(2017, 5, 1)
        week_route_info = WeekRouteInfo(monday)
        route_info = {'day': 'monday', 'services': 'all', 'contractor': 'gfl', 'week': 'a', 'FID': 0}
        week_route_info.add_day_route(route_info)
        expected = {0: {'contractor': 'gfl', 'week': 'a', 'services': 'all'}}
        self.assertEqual(expected, week_route_info.data[0], "WeekRouteInfo.add_day_route() adds a day's worth of route info")

    def test_reschedule_service_all(self):

        monday = datetime.datetime(2017, 5, 1)
        week_route_info = WeekRouteInfo(monday)
        route_info = {'day': 'monday', 'services': 'all', 'contractor': 'gfl', 'week': 'a', 'FID': 0}
        week_route_info.add_day_route(route_info)
        week_route_info.reschedule_service(monday, datetime.datetime(2017, 5, 2), 'all')
        self.assertEqual({}, week_route_info.data[0], "WeekRouteInfo.reschedule_service() cancels original day's service")
        expected = {0: {'contractor': 'gfl', 'week': 'a', 'services': 'all'}}
        self.assertEqual(expected, week_route_info.data[1], "WeekRouteInfo.reschedule_service() reschedules service")

    def test_reschedule_service_trash(self):

        monday = datetime.datetime(2017, 5, 1)
        week_route_info = WeekRouteInfo(monday)
        route_info = {'day': 'monday', 'services': 'all',   'contractor': 'gfl',     'week': 'a', 'FID': 0}
        week_route_info.add_day_route(route_info)
        route_info = {'day': 'monday', 'services': 'trash', 'contractor': 'advance', 'week': ' ', 'FID': 14}
        week_route_info.add_day_route(route_info)

        week_route_info.reschedule_service(monday, datetime.datetime(2017, 5, 2), 'trash')
        self.assertEqual({}, week_route_info.data[0], "WeekRouteInfo.reschedule_service() cancels original day's trash service")
        expected = {0: {'contractor': 'gfl', 'week': 'a', 'services': 'all'}, 14: {'contractor': 'advance', 'week': ' ', 'services': 'trash'}}
        self.assertEqual(expected, week_route_info.data[1], "WeekRouteInfo.reschedule_service() reschedules trash service")

    def test_get_day(self):

        monday = datetime.datetime(2017, 5, 8)
        week_route_info = WeekRouteInfo(monday)
        route_info = {'day': 'monday', 'services': 'all', 'contractor': 'gfl', 'week': 'b', 'FID': 0}
        week_route_info.add_day_route(route_info)
        expected = {0: {'contractor': 'gfl', 'week': 'b', 'services': 'all'}}
        self.assertEqual(expected, week_route_info.get_day(monday), "WeekRouteInfo.get_day() returns a day's worth of route info")


class WasteScheduleTests(TestCase):

    def setUp(self):
        """
        Set up each unit test, including making sure database is properly cleaned up before each test
        """
        cleanup_db()
        self.maxDiff = None

    def test_schedule_detail_str(self):
        detail = make_schedule_detail(detail_type='schedule', service_type=ScheduleDetail.TRASH, normal_day=datetime.date(2017, 5, 1), new_day=datetime.date(2017, 5, 2))
        self.assertTrue(str(detail).find('schedule') >= 0 and str(detail).find(ScheduleDetail.TRASH) >= 0)

    def test_schedule_detail_validation(self):

        values = [
            { "detail_type": "schedule", "service_type": "recycling", "normal_day": datetime.date(2017, 1, 1), "new_day": None },
            { "detail_type": "schedule", "service_type": "recycling", "normal_day": None,                      "new_day": datetime.date(2017, 1, 1) },
            { "detail_type": "schedule", "service_type": "recycle",   "normal_day": datetime.date(2017, 1, 1), "new_day": datetime.date(2017, 1, 1) },
            { "detail_type": "invalid",  "service_type": "recycling", "normal_day": datetime.date(2017, 1, 1), "new_day": datetime.date(2017, 1, 1) },
            { "detail_type": "invalid",  "service_type": "recycling", "normal_day": None,                      "new_day": None },
        ]

        for value in values:
            with self.assertRaises(ValidationError, msg="Invalid schedule detail raises an error") as error:
                make_schedule_detail(**value)

    def util_test_get_next_pickups(self, today, route_ids, expected):
        """
        Utility function to run test pickups
        """
        
        c = Client()
        response = c.get("/waste_schedule/details/{0}/?today={1}".format(route_ids, today))

        self.assertTrue(response.status_code == 200)
        self.assertDictEqual(expected, response.data, "Routes {} should get it's pickups predicted correctly".format(route_ids))

    def test_map_service_type(self):
        self.assertTrue(ScheduleDetail.map_service_type('trash') == 'trash', "map_service_type() maps trash to trash")

    def test_map_service_type_all(self):
        self.assertTrue(ScheduleDetail.map_service_type('all') == 'all', "map_service_type() maps recycle to recycling")

    def test_map_service_type_recycle(self):
        self.assertTrue(ScheduleDetail.map_service_type('recycle') == 'recycling', "map_service_type() maps recycling to recycle")

    def test_is_same_service_type(self):
        self.assertTrue(ScheduleDetail.is_same_service_type('trash', 'trash'), "is_same_service_type() equates 'trash' with 'trash'")

    def test_is_same_service_type_recycle(self):
        self.assertTrue(ScheduleDetail.is_same_service_type('recycling', 'recycle'), "is_same_service_type() equates 'recycling' with 'recycle'")

    def test_is_same_service_type_all1(self):
        self.assertTrue(ScheduleDetail.is_same_service_type('bulk', 'all'), "is_same_service_type() equates 'all' with 'bulk'")

    def test_is_same_service_type_all2(self):
        self.assertTrue(ScheduleDetail.is_same_service_type('all', 'bulk'), "is_same_service_type() equates 'bulk' with 'all'")

    def test_get_next_oneday_pickups(self):
        """
        Test getting next pickups for routes that have all pickups on the same day (e.g., route 8)
        """

        values = {
            0: {'next_pickups': {'recycling': {'route': 0, 'next_pickup': '2017-05-08T00:00:00', 'day': 'monday', 'contractor': 'gfl', 'week': 'b'}, 'trash': {'route': 0, 'next_pickup': '2017-05-01T00:00:00', 'day': 'monday', 'contractor': 'gfl', 'week': 'b'}, 'bulk': {'route': 0, 'next_pickup': '2017-05-08T00:00:00', 'day': 'monday', 'contractor': 'gfl', 'week': 'b'}}, 'details': []},
            8: {'next_pickups': {'recycling': {'route': 8, 'next_pickup': '2017-05-05T00:00:00', 'day': 'friday', 'contractor': 'gfl', 'week': 'a'}, 'trash': {'route': 8, 'next_pickup': '2017-04-28T00:00:00', 'day': 'friday', 'contractor': 'gfl', 'week': 'a'}, 'bulk': {'route': 8, 'next_pickup': '2017-05-05T00:00:00', 'day': 'friday', 'contractor': 'gfl', 'week': 'a'}}, 'details': []},
            9: {'next_pickups': {'recycling': {'route': 9, 'next_pickup': '2017-04-28T00:00:00', 'day': 'friday', 'contractor': 'gfl', 'week': 'b'}, 'trash': {'route': 9, 'next_pickup': '2017-04-28T00:00:00', 'day': 'friday', 'contractor': 'gfl', 'week': 'b'}, 'bulk': {'route': 9, 'next_pickup': '2017-04-28T00:00:00', 'day': 'friday', 'contractor': 'gfl', 'week': 'b'}}, 'details': []},
        }

        today = "20170427"

        for route_id in values.keys():
            self.util_test_get_next_pickups(today, route_id, values[route_id])

    def test_get_next_multiday_pickups(self):
        """
        Test getting next pickups for routes that have all pickups on different days (e.g., route 8)
        """

        values = {
            '11,28,35': {'next_pickups': {'bulk': {'next_pickup': '2017-05-04T00:00:00', 'week': 'a', 'day': 'thursday', 'contractor': 'advance', 'route': 35}, 'trash': {'next_pickup': '2017-05-03T00:00:00', 'week': ' ', 'day': 'wednesday', 'contractor': 'advance', 'route': 11}, 'recycling': {'next_pickup': '2017-04-27T00:00:00', 'week': 'b', 'day': 'thursday', 'contractor': 'advance', 'route': 28}}, 'details': []},
            '14,27,31': {'next_pickups': {'recycling': {'week': 'a', 'day': 'monday', 'contractor': 'advance', 'route': 27, 'next_pickup': '2017-05-01T00:00:00'}, 'bulk': {'week': 'a', 'day': 'tuesday', 'contractor': 'advance', 'route': 31, 'next_pickup': '2017-05-02T00:00:00'}, 'trash': {'week': ' ', 'day': 'monday', 'contractor': 'advance', 'route': 14, 'next_pickup': '2017-05-01T00:00:00'}}, 'details': []},
        }

        today = "20170427"

        for route_ids in values.keys():
            self.util_test_get_next_pickups(today, route_ids, values[route_ids])

    def test_get_next_oneday_pickups_yard_waste(self):
        """
        Test getting next pickups for routes that have all pickups on the same day (e.g., route 8),
        with yard waste active
        """

        make_schedule_detail(detail_type='start-date', service_type=ScheduleDetail.YARD_WASTE, new_day=datetime.date(2017, 3, 1))
        make_schedule_detail(detail_type='end-date', service_type=ScheduleDetail.YARD_WASTE, new_day=datetime.date(2017, 11, 1))

        values = {
            0: {'next_pickups': {'recycling': {'route': 0, 'next_pickup': '2017-05-08T00:00:00', 'day': 'monday', 'contractor': 'gfl', 'week': 'b'}, 'trash': {'route': 0, 'next_pickup': '2017-05-01T00:00:00', 'day': 'monday', 'contractor': 'gfl', 'week': 'b'}, 'bulk': {'route': 0, 'next_pickup': '2017-05-08T00:00:00', 'day': 'monday', 'contractor': 'gfl', 'week': 'b'}, 'yard waste': {'route': 0, 'next_pickup': '2017-05-08T00:00:00', 'day': 'monday', 'contractor': 'gfl', 'week': 'b'}}, 'details': [{'description': '', 'note': None, 'newDay': '2017-03-01T00:00:00', 'service': 'yard waste', 'normalDay': '', 'type': 'start-date', 'wasteAreaIds': ''}, {'description': '', 'note': None, 'newDay': '2017-11-01T00:00:00', 'service': 'yard waste', 'normalDay': '', 'type': 'end-date', 'wasteAreaIds': ''}]},
            8: {'next_pickups': {'recycling': {'route': 8, 'next_pickup': '2017-05-05T00:00:00', 'day': 'friday', 'contractor': 'gfl', 'week': 'a'}, 'trash': {'route': 8, 'next_pickup': '2017-04-28T00:00:00', 'day': 'friday', 'contractor': 'gfl', 'week': 'a'}, 'bulk': {'route': 8, 'next_pickup': '2017-05-05T00:00:00', 'day': 'friday', 'contractor': 'gfl', 'week': 'a'}, 'yard waste': {'route': 8, 'next_pickup': '2017-05-05T00:00:00', 'day': 'friday', 'contractor': 'gfl', 'week': 'a'}}, 'details': [{'description': '', 'note': None, 'newDay': '2017-03-01T00:00:00', 'service': 'yard waste', 'normalDay': '', 'type': 'start-date', 'wasteAreaIds': ''}, {'description': '', 'note': None, 'newDay': '2017-11-01T00:00:00', 'service': 'yard waste', 'normalDay': '', 'type': 'end-date', 'wasteAreaIds': ''}]},
            9: {'next_pickups': {'recycling': {'route': 9, 'next_pickup': '2017-04-28T00:00:00', 'day': 'friday', 'contractor': 'gfl', 'week': 'b'}, 'trash': {'route': 9, 'next_pickup': '2017-04-28T00:00:00', 'day': 'friday', 'contractor': 'gfl', 'week': 'b'}, 'bulk': {'route': 9, 'next_pickup': '2017-04-28T00:00:00', 'day': 'friday', 'contractor': 'gfl', 'week': 'b'}, 'yard waste': {'route': 9, 'next_pickup': '2017-04-28T00:00:00', 'day': 'friday', 'contractor': 'gfl', 'week': 'b'}}, 'details': [{'description': '', 'note': None, 'newDay': '2017-03-01T00:00:00', 'service': 'yard waste', 'normalDay': '', 'type': 'start-date', 'wasteAreaIds': ''}, {'description': '', 'note': None, 'newDay': '2017-11-01T00:00:00', 'service': 'yard waste', 'normalDay': '', 'type': 'end-date', 'wasteAreaIds': ''}]},
        }

        today = "20170427"

        for route_id in values.keys():
            self.util_test_get_next_pickups(today, route_id, values[route_id])

    def test_get_next_multiday_pickups_yard_waste(self):
        """
        Test getting next pickups for routes that have all pickups on different days (e.g., route 8),
        with yard waste active
        """

        make_schedule_detail(detail_type='start-date', service_type=ScheduleDetail.YARD_WASTE, new_day=datetime.date(2017, 3, 1))
        make_schedule_detail(detail_type='end-date', service_type=ScheduleDetail.YARD_WASTE, new_day=datetime.date(2017, 11, 1))

        values = {
            '11,28,35': {'next_pickups': {'bulk': {'next_pickup': '2017-05-04T00:00:00', 'week': 'a', 'day': 'thursday', 'contractor': 'advance', 'route': 35}, 'yard waste': {'next_pickup': '2017-05-04T00:00:00', 'week': 'a', 'day': 'thursday', 'contractor': 'advance', 'route': 35}, 'trash': {'next_pickup': '2017-05-03T00:00:00', 'week': ' ', 'day': 'wednesday', 'contractor': 'advance', 'route': 11}, 'recycling': {'next_pickup': '2017-04-27T00:00:00', 'week': 'b', 'day': 'thursday', 'contractor': 'advance', 'route': 28}}, 'details': [{'wasteAreaIds': '', 'normalDay': '', 'newDay': '2017-03-01T00:00:00', 'type': 'start-date', 'service': 'yard waste', 'description': '', 'note': None}, {'wasteAreaIds': '', 'normalDay': '', 'newDay': '2017-11-01T00:00:00', 'type': 'end-date', 'service': 'yard waste', 'description': '', 'note': None}]},
            '14,27,31': {'next_pickups': {'recycling': {'week': 'a', 'day': 'monday', 'contractor': 'advance', 'route': 27, 'next_pickup': '2017-05-01T00:00:00'}, 'bulk': {'week': 'a', 'day': 'tuesday', 'contractor': 'advance', 'route': 31, 'next_pickup': '2017-05-02T00:00:00'}, 'yard waste': {'week': 'a', 'day': 'tuesday', 'contractor': 'advance', 'route': 31, 'next_pickup': '2017-05-02T00:00:00'}, 'trash': {'week': ' ', 'day': 'monday', 'contractor': 'advance', 'route': 14, 'next_pickup': '2017-05-01T00:00:00'}}, 'details': [{'wasteAreaIds': '', 'normalDay': '', 'newDay': '2017-03-01T00:00:00', 'type': 'start-date', 'service': 'yard waste', 'description': '', 'note': None}, {'wasteAreaIds': '', 'normalDay': '', 'newDay': '2017-11-01T00:00:00', 'type': 'end-date', 'service': 'yard waste', 'description': '', 'note': None}]},
        }

        today = "20170427"

        for route_ids in values.keys():
            self.util_test_get_next_pickups(today, route_ids, values[route_ids])

    def util_get_schedule_details(self, route_ids, expected):

        c = Client()
        response = c.get("/waste_schedule/details/{}/?today=20170428".format(route_ids))
        self.assertTrue(response.status_code == 200)
        self.assertDictEqual(expected, response.data, "Routes {} should receive proper data".format(route_ids))

    def test_get_schedule_details_auto_today(self):
        """
        Get today's pickups, allowing the api to figure out what 'today' is
        """
        
        c = Client()
        response = c.get("/waste_schedule/details/0/")
        self.assertTrue(response.status_code == 200)

    def test_get_schedule_details(self):

        values = {
            "0": {'next_pickups': {'bulk': {'day': 'monday', 'route': 0, 'contractor': 'gfl', 'next_pickup': '2017-05-08T00:00:00', 'week': 'b'}, 'recycling': {'day': 'monday', 'route': 0, 'contractor': 'gfl', 'next_pickup': '2017-05-08T00:00:00', 'week': 'b'}, 'trash': {'day': 'monday', 'route': 0, 'contractor': 'gfl', 'next_pickup': '2017-05-01T00:00:00', 'week': 'b'}}, 'details': []},
            "8": {'next_pickups': {'bulk': {'day': 'friday', 'route': 8, 'contractor': 'gfl', 'next_pickup': '2017-05-05T00:00:00', 'week': 'a'}, 'recycling': {'day': 'friday', 'route': 8, 'contractor': 'gfl', 'next_pickup': '2017-05-05T00:00:00', 'week': 'a'}, 'trash': {'day': 'friday', 'route': 8, 'contractor': 'gfl', 'next_pickup': '2017-04-28T00:00:00', 'week': 'a'}}, 'details': []},
            "9": {'next_pickups': {'bulk': {'day': 'friday', 'route': 9, 'contractor': 'gfl', 'next_pickup': '2017-04-28T00:00:00', 'week': 'b'}, 'recycling': {'day': 'friday', 'route': 9, 'contractor': 'gfl', 'next_pickup': '2017-04-28T00:00:00', 'week': 'b'}, 'trash': {'day': 'friday', 'route': 9, 'contractor': 'gfl', 'next_pickup': '2017-04-28T00:00:00', 'week': 'b'}}, 'details': []},
        }

        for route_ids, expected in values.items():
            self.util_get_schedule_details(route_ids, expected)

    def test_get_schedule_details_today(self):

        c = Client()
        response = c.get("/waste_schedule/details/0/?today=20170501")
        self.assertTrue(response.status_code == 200)
        expected = {'details': [], 'next_pickups': {'recycling': {'day': 'monday', 'contractor': 'gfl', 'week': 'b', 'next_pickup': '2017-05-08T00:00:00', 'route': 0}, 'bulk': {'day': 'monday', 'contractor': 'gfl', 'week': 'b', 'next_pickup': '2017-05-08T00:00:00', 'route': 0}, 'trash': {'day': 'monday', 'contractor': 'gfl', 'week': 'b', 'next_pickup': '2017-05-01T00:00:00', 'route': 0}}}
        self.assertDictEqual(expected, response.data, "Query param 'today' indicates date we are interested in")

    def test_get_schedule_details_by_month_year(self):

        c = Client()
        response = c.get("/waste_schedule/details/0/year/2017/month/7/?today=20170428")
        self.assertTrue(response.status_code == 200)
        expected = {'next_pickups': {'bulk': {'day': 'monday', 'route': 0, 'contractor': 'gfl', 'next_pickup': '2017-05-08T00:00:00', 'week': 'b'}, 'trash': {'day': 'monday', 'route': 0, 'contractor': 'gfl', 'next_pickup': '2017-05-01T00:00:00', 'week': 'b'}, 'recycling': {'day': 'monday', 'route': 0, 'contractor': 'gfl', 'next_pickup': '2017-05-08T00:00:00', 'week': 'b'}}, 'details': []}
        self.assertDictEqual(expected, response.data, "waste_schedule/details can be filtered by year and month")

    def test_get_schedule_details_invalid_params(self):

        c = Client()
        response = c.get("/waste_schedule/details/0/?invalid=yes")
        self.assertTrue(response.status_code == 400, "Passing invalid parameter to endpoint generates error")

    def test_get_schedule_details_citywide_reschedule(self):

        c = Client()
        make_schedule_detail(detail_type='schedule', service_type=ScheduleDetail.TRASH, normal_day=datetime.date(2017, 5, 1), new_day=datetime.date(2017, 5, 2))
        response = c.get("/waste_schedule/details/0/?today=20170501")
        self.assertTrue(response.status_code == 200)
        expected = {'details': [{'note': ' (other service conflicts: recycling for ,1,27, and bulk/hazardous/yard waste for ,1,29,)', 'service': 'trash', 'normalDay': '2017-05-01T00:00:00', 'wasteAreaIds': ',0,1,14,', 'newDay': '2017-05-02T00:00:00', 'description': '', 'type': 'schedule'}], 'next_pickups': {'trash': {'next_pickup': '2017-05-02T00:00:00', 'week': 'b', 'route': 0, 'day': 'monday', 'contractor': 'gfl'}, 'recycling': {'next_pickup': '2017-05-08T00:00:00', 'week': 'b', 'route': 0, 'day': 'monday', 'contractor': 'gfl'}, 'bulk': {'next_pickup': '2017-05-08T00:00:00', 'week': 'b', 'route': 0, 'day': 'monday', 'contractor': 'gfl'}}}
        self.assertDictEqual(expected, response.data, "Waste schedule reschedules services around schedule changes")

    def test_schedule_detail_mgr_init(self):
        ScheduleDetailMgr.instance()
        with self.assertRaises(Exception, msg="Invoking ScheduleDetailMgr() raises an exception") as error:
            ScheduleDetailMgr()

    def test_schedule_detail_mgr_singleton(self):
        self.assertEqual(id(ScheduleDetailMgr.instance()), id(ScheduleDetailMgr.instance()), "Only one instance of SchedulDetailMgr exists")

    def test_schedule_detail_mgr_service_dates(self):
        start_test = make_schedule_detail(detail_type='start-date', service_type=ScheduleDetail.YARD_WASTE, new_day=datetime.date(2017, 3, 1))
        end_test = make_schedule_detail(detail_type='end-date', service_type=ScheduleDetail.YARD_WASTE, new_day=datetime.date(2017, 11, 1))
        start, end = ScheduleDetailMgr.instance().get_service_start_and_end('yard waste')

        self.assertEqual(start.new_day, start_test.new_day, "get_service_start_and_end() returns start date for a service")
        self.assertEqual(end.new_day, end_test.new_day, "get_service_start_and_end() returns end date for a service")

    def test_schedule_detail_mgr_service_dates_none(self):
        start, end = ScheduleDetailMgr.instance().get_service_start_and_end('yard waste')
        self.assertTrue(start == None and end == None, "We get None back for start and end dates when they don't exist for a service")

    def test_is_service_active_trash(self):
        self.assertTrue(ScheduleDetailMgr.instance().is_service_active('trash', datetime.date(2017, 7, 1)), "Year round services are active")

    def test_is_service_active_yard_waste(self):
        make_schedule_detail(detail_type='start-date', service_type=ScheduleDetail.YARD_WASTE, new_day=datetime.date(2017, 3, 1))
        make_schedule_detail(detail_type='end-date', service_type=ScheduleDetail.YARD_WASTE, new_day=datetime.date(2017, 11, 1))
        self.assertTrue(ScheduleDetailMgr.instance().is_service_active('yard waste', datetime.date(2017, 7, 1)), "Yard waste is active between start and end")

    def test_is_service_active_yard_waste_too_late(self):
        make_schedule_detail(detail_type='start-date', service_type=ScheduleDetail.YARD_WASTE, new_day=datetime.date(2017, 3, 1))
        make_schedule_detail(detail_type='end-date', service_type=ScheduleDetail.YARD_WASTE, new_day=datetime.date(2017, 11, 1))
        self.assertFalse(ScheduleDetailMgr.instance().is_service_active('yard waste', datetime.date(2017, 12, 1)), "Yard waste is inactive after end")

    def test_is_service_active_default(self):
        self.assertFalse(ScheduleDetailMgr.instance().is_service_active('yard waste', datetime.date(2017, 7, 1)), "When service start and end dates are not set up it is inactive")
