from datetime import date, timedelta

from django.shortcuts import render

from dnninternet.models import Faqs, Htmltext

from cod_utils.util import date_json


def parse_date(val):

    return datetime.strptime(val, "%Y%m%d").date()


@api_view(['GET'])
def get_amount_added(request, start=None, end=None, format=None):

    if start:

        start = parse_date(start)
        
    else:

        # default: most-recent monday
        today = date.today()
        diff = today.weekday()
        if diff == 0:
            start = today
        else:
            start = today - timedelta(days=diff)

    if end:

        end = parse_date(end)

    else:

        # default: most-recent sunday
        end = start + timedelta(days=6)

    faqs = Faqs.objects.filter(DateModified__range = (start, end))
    pages = Htmltext.objects.filter(LastModifiedOnDate__range = (start, end))

    content = {
        "num_faqs": len(faqs),
        "num_html_pages": len(pages),
        "date_start": date_json(start),
        "date_end": date_json(end),
        "num_days": (end - start).days,
    }

    return Response(content)
