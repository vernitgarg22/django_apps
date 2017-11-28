import datetime

from waste_schedule.models import BiWeekType, ScheduleDetail


def check_month_val(year, month, date):
    """
    Returns True if the date object belongs to the given month
    and year.  If date is null, returns False
    """

    if not date:
        return False
    if year:
        if date.year != int(year):
            return False
    if month:
        if date.month != int(month):
            return False
    return True

def check_month(year, month, detail):
    """
    Returns True if the ScheduleDetail object belongs to the given month
    and year, or is a start-date and end-date ScheduleDetail objects.
    """

    if detail.detail_type == 'start-date' or detail.detail_type == 'end-date':
        return True
    return check_month_val(year, month, detail.normal_day) or check_month_val(year, month, detail.new_day)

def filter_month(year, month, details):
    """
    Returns list of ScheduleDetail objects belonging to the given month and year,
    as well as start-date and end-date ScheduleDetail objects.
    """

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

def map_service_type(service):
    """
    Maps gis server service names to the names in use here:
    In particular 'recycle' becomes 'recycling'.
    """
    return ScheduleDetail.RECYCLING if service == 'recycle' else service
