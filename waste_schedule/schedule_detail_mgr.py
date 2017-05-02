import datetime

from waste_schedule.models import ScheduleDetail


class ScheduleDetailMgr():

    # the one and only singlton instance of the ScheduleDetailMgr
    __instance = None

    def __init__(self):
        # Make sure only 1 instance of ScheduleDetailMgr is created
        if ScheduleDetailMgr.__instance:
            raise Exception("call ScheduleDetailMgr.instance() to get access to ScheduleDetailMgr")

    def instance():
        """
        Should return one-and-only instance of this class
        """
        if ScheduleDetailMgr.__instance is None:
            ScheduleDetailMgr.__instance = ScheduleDetailMgr()
        return ScheduleDetailMgr.__instance

    def get_service_start_and_end(self, service):
        """
        Returns the ScheduleDetail objects that indicate when the given
        service starts and ends
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
