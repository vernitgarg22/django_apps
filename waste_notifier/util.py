import datetime

from waste_schedule.models import ScheduleDetail
from waste_schedule.schedule_detail_mgr import ScheduleDetailMgr
from cod_utils import util


def includes_yard_waste(services):
    """
    Returns True if one of the services includes yard waste.  Note that yard_waste
    currently occurs on same schedule as bulk, so we are treating bulk pickup as including
    yard waste pickup
    """
    return ScheduleDetail.ALL in services or ScheduleDetail.YARD_WASTE in services or ScheduleDetail.BULK in services

def add_additional_services(services, date):
    """
    Add in any services that are implicitly included in this list of services
    (e.g., yard waste is included whenever bulk is in the list).
    Note:  services that are not year-round should only be included if they
    are active for the given date
    """
    if ScheduleDetail.ALL in services:
        services = ScheduleDetail.YEAR_ROUND_SERVICES

    # Special handling for yard waste, since it is on same schedule as bulk
    if includes_yard_waste(services) and ScheduleDetailMgr.instance().is_service_active(ScheduleDetail.YARD_WASTE, date):
        services.append(ScheduleDetail.YARD_WASTE)

    return services

def get_services_desc(services):
    """
    Returns comma-delimited list of services, with last comma replaced by 'and'.
    Input should be a list of services.
    """

    # build comma-delimited list of services
    desc = ''.join([ service + ', ' for service in sorted(set(services)) ])

    # remove trailing comma
    desc = desc[:-2]

    # if more than 1 service, replace last comma with 'and'
    if len(services) > 1:
        index = desc.rfind(',')
        desc = desc[0: index] + " and" + desc[index + 1: ]

    return desc

def get_service_message(services, date):
    """
    Returns message to be sent to subscriber, including correct list of services and date
    """
    services = add_additional_services(services, date)
    return "City of Detroit Public Works:  Your next pickup for {0} is {1}".format(get_services_desc(services), date.strftime("%b %d, %Y"))

def get_service_detail_message(services, detail):
    """
    Returns message to be sent to subscriber, including correct list of services and informtion about service detail
    (e.g., schedule change)
    """

    message = 'City of Detroit Public Works:  '
    detail_desc = ''
    if detail.detail_type == 'schedule':
        detail_desc = "Your pickup for {0} for {1} is postponed to {2} due to {3}".format(get_services_desc(services), 
            detail.normal_day.strftime("%b %d, %Y"), detail.new_day.strftime("%b %d, %Y"), detail.description)
    elif detail.detail_type == 'info':
        detail_desc = detail.description
    elif detail.detail_type == 'start-date' or detail.detail_type == 'end-date':
        detail_desc = detail.description + ' ' + detail.new_day.strftime("%b %d, %Y")

    message = message + detail_desc
    if detail.note:
        message = message + " - " + detail.note

    return message


class SubscriberServices:
    """
    Keeps track of what subscribes are supposed to receive a notification
    """

    def __init__(self):

        # map of subscribers receiving notifications
        self.subscribers = {}

        # map subscribers to the services for which they are receiving notifications
        self.services = {}

        # map services and routes to the subscribers receiving notifications for each service
        self.service_subscribers = {}

    def add(self, subscribers, service_type, route_ids):
        """
        Keep track of what notifications were sent to what subscribers.
        Specifically, keep a map of subscribers getting notifications, and
        keep a list of services getting notifications for each subscriber.
        """

        if type(route_ids) == str:
            route_ids = util.split_csv(route_ids)

        for subscriber in subscribers:
            self.subscribers[subscriber.phone_number] = subscriber
            services_list = self.services.get(subscriber.phone_number) or []
            services_list.extend([service_type])
            self.services[subscriber.phone_number] = services_list

        if not self.service_subscribers.get(service_type):
            self.service_subscribers[service_type] = {}

        if route_ids == []:
            self.service_subscribers[service_type][''] = subscribers
        else:
            for route_id in route_ids:
                self.service_subscribers[service_type][route_id] = subscribers

    def get_subscribers(self):
        """
        Return container of all subscribers getting notifications
        """
        return self.subscribers.values()

    def get_service_subscribers(self):
        """
        Return container of all subscribers getting notifications for the
        particular service.
        """
        return self.service_subscribers

    def get_services(self, subscriber):
        """
        Get list of services for which the given subscriber
        is receiving alerts
        """
        return self.services[subscriber.phone_number]


class SubscriberServicesDetail(SubscriberServices):
    """
    Keeps track of what subscribes are supposed to receive a notification
    about a schedule change
    """

    def __init__(self, schedule_detail, subscribers, service, route_ids):
        super().__init__()
        self.schedule_detail = schedule_detail
        for subscriber in subscribers:
            self.add(subscribers, service, route_ids)


class NotificationContent():
    """
    Records information about notifications sent out
    """

    def __init__(self, subscribers_services, subscribers_services_details, date_applicable, dry_run):

        # TODO output what type of reminder was sent out?
        # - normal weekly reminder
        # - schedule change
        # - info only notice
        # - start or end date

        self.content = {
            "meta": {
                "date_applicable": date_applicable.strftime("%Y-%m-%d"),
                "current_time": datetime.datetime.today().strftime("%Y-%m-%d %H:%M"),
                "dry_run": dry_run,
            },
            "citywide": {}
        }


        # indicate, by route, which phone numbers we have texted
        service_subscribers_map = subscribers_services.get_service_subscribers()
        ssm = service_subscribers_map


        for service_type, routes in service_subscribers_map.items():
            for route_id, subscribers in routes.items():
                if not self.content.get(service_type):
                    self.content[service_type] = {}
                self.content[service_type].update({ route_id: { subscriber.phone_number: 1 for subscriber in subscribers } })

        # indicate which phone numbers we have sent citywide alerts to
        for subscribers_services_detail in subscribers_services_details:
            service_subscribers = subscribers_services_detail.get_service_subscribers()
            for service_type, routes in service_subscribers.items():
                for route_id, subscribers in routes.items():
                    if route_id == '':
                        self.content["citywide"].update( { subscriber.phone_number: 1 for subscriber in subscribers } )

    def get_content(self):
        return self.content