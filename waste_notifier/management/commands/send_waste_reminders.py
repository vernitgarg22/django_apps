from datetime import date
import re

from django.core.management.base import BaseCommand, CommandError

from cod_utils import util
from cod_utils.messaging import MsgHandler

from waste_notifier import views


class Command(BaseCommand):
    help = """
        Use this to send out waste pickup reminders, e.g.,
        python manage.py send_waste_reminders  """

    def add_arguments(self, parser):
        parser.add_argument('--tomorrow', default=util.tomorrow(), help="Date value to treat as tomorrow. Format=YYYYMMDD")
        parser.add_argument('--dry_run', default='no', help="Pass 'yes' to do a dry run")

    def handle(self, *args, **options):

        # Validate and parse our command-line params
        tomorrow = options['tomorrow']
        dry_run_param = options['dry_run']

        if dry_run_param not in ['yes', 'no']:
            raise CommandError("--dry_run must be 'yes' or 'no'")

        if type(tomorrow) == str:
            if not re.fullmatch(r'^\d{8}$', tomorrow):
                raise CommandError("Date format for tomorrow must be YYYYMMDD")
            tomorrow = date(int(tomorrow[0:4]), int(tomorrow[4:6]), int(tomorrow[6:8]))

        response = views.send_notifications(date=tomorrow, dry_run_param=True)

        return "Status: {}, data: {}".format(response.status_code, str(response.data))
