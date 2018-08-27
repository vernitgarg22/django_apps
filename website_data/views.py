from datetime import datetime, date, timedelta
import pytz

from django.shortcuts import render
from django.utils import timezone

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from dnninternet.models import Faqs, Htmltext
from waste_notifier.models import Subscriber

from cod_utils.util import date_json


def parse_date(val):

    dt = datetime.strptime(val, "%Y%m%d")
    dt = timezone.make_aware(dt)
    return dt.date()


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

    num_faqs = Faqs.objects.filter(datemodified__range = (start, end)).count()
    num_pages = Htmltext.objects.filter(lastmodifiedondate__range = (start, end)).count()
    total_subscribers = Subscriber.objects.filter(status='active').count()
    new_subscribers = Subscriber.objects.filter(status='active').filter(created_at__range = (start, end)).count()

    content = {
        "date_start": date_json(start),
        "date_end": date_json(end),
        "num_days": (end - start).days,
        "website_analytics": {
            "num_faqs": num_faqs,
            "num_html_pages": num_pages,
        },
        "waste_reminders": {
            "total_subscribers": total_subscribers,
            "new_subscribers": new_subscribers,
        }
    }

    return Response(content)
