from datetime import datetime, date, timedelta
import pytz
import time

from django.shortcuts import render
from django.utils import timezone

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from waste_notifier.models import Subscriber

# from website_data.website_db_engine import WebsiteDBEngine

from cod_utils.util import date_json


def parse_date(val):

    dt = datetime.strptime(val, "%Y%m%d")
    dt = timezone.make_aware(dt)
    return dt.date()


def get_page_count(start=None, end=None):

    return 0

    # node_count = 0
    # term_count = 0
    # engine = WebsiteDBEngine('detroitmi.prod')
    # try:
    #     engine.start()
    #     if start and end:
    #         start_seconds = int(time.mktime(start.timetuple()))
    #         end_seconds = int(time.mktime(end.timetuple()))
    #         results = engine.get(
    #             "select count(distinct n.nid) as 'count' "
    #             "from node n join node_revision nr on n.nid = nr.nid "
    #             "where type in :types and revision_timestamp between :start and :end ;",
    #             types=('faq', 'how_do_i', 'page', 'story', 'web_apps'), start=start_seconds, end=end_seconds)
    #     else:
    #         results = engine.get(
    #                 "select count(distinct n.nid) as 'count' "
    #                 "from node n join node_revision nr on n.nid = nr.nid "
    #                 "where type in :types ;",
    #                 types=('faq', 'how_do_i', 'page', 'story', 'web_apps'))

    #     node_count = results[0]['count']

    #     results = engine.get("select count(distinct tid) as 'count' from taxonomy_term_data where langcode = :lang ;", lang='en')
    #     term_count = results[0]['count']

    # except:
    #     return 0

    # finally:
    #     engine.stop()
    #     return node_count + term_count

@api_view(['GET'])
def get_new_content(request, start=None, end=None, format=None):

    if start:

        start = parse_date(start)

    else:

        # default: most-recent monday
        today = timezone.now().date()
        diff = today.weekday()

        if diff == 0:
            diff = 7

        start = today - timedelta(days=diff)

    if end:

        end = parse_date(end)

    else:

        # default: most-recent sunday
        end = start + timedelta(days=6)

    num_total_pages = get_page_count()
    num_new_pages = get_page_count(start=start, end=end)

    num_total_subscribers = Subscriber.objects.filter(status='active').count()
    num_new_subscribers = Subscriber.objects.filter(status='active').filter(created_at__range = (start, end)).count()

    content = {
        "date_start": date_json(start),
        "date_end": date_json(end),
        "num_days": (end - start).days,
        "website_analytics": {
            "num_new_html_pages": num_new_pages,
            "num_total_html_pages": num_total_pages,
        },
        "waste_reminders": {
            "total_subscribers": num_total_subscribers,
            "new_subscribers": num_new_subscribers,
        }
    }

    return Response(content)

@api_view(['GET'])
def get_subscriber_metadata(request, start=None, end=None, format=None):
    """
Returns metadata about people who have recently subscribed to
curbside waste pickup reminders:

* e.g.,
    * https://apis.detroitmi.gov/website_data/waste_subscribers/
    * https://apis.detroitmi.gov/website_data/waste_subscribers/20190601/
    * https://apis.detroitmi.gov/website_data/waste_subscribers/20190601/20190610/

* optional parameters:
    * start-date - start date of the time window to query (default is 1 week ago) - format YYYYMMDD
    * end-date - end date of the time window to query (default is today) - format YYYYMMDD
    """

    # Parse our date filters
    if start:

        start = parse_date(start)

    else:

        # default start date:  1 week ago
        start = date.today() - timedelta(days=7)

    if end:

        end = parse_date(end)

    else:

        # default end date:  today
        end = date.today()

    subscribers = Subscriber.objects.filter(status='active').filter(last_status_update__range = (start, end))

    content = {
        "filters": {
            "start-date": date_json(start),
            "end-date": date_json(end),
        },
        "subscriber_metadata": []
    }

    for subscriber in subscribers:

        tmp = {
            "address": subscriber.address,
            "lat": subscriber.latitude,
            "lon": subscriber.longitude,
        }
        content["subscriber_metadata"] += [tmp]

    return Response(content)
