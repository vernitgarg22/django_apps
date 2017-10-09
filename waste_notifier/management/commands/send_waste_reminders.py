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
        parser.add_argument('--today', default=date.today(), help="Date value to treat as today. Format=YYYYMMDD")
        parser.add_argument('--dry_run', default='no', help="Pass 'yes' to do a dry run")

    def handle(self, *args, **options):

        # Validate and parse our command-line params
        today = options['today']
        dry_run_param = options['dry_run']

        if dry_run_param not in ['yes', 'no']:
            raise CommandError("--dry_run must be 'yes' or 'no'")

        if type(today) == str:
            if not re.fullmatch(r'^\d{8}$', today):
                raise CommandError("Date format for 'today' must be YYYYMMDD")
            today = date(int(today[0:4]), int(today[4:6]), int(today[6:8]))
        elif not type(today) == date:    # pragma: no cover (should never get here)
            raise CommandError("Invalid data type for today param")

        response = views.send_notifications(date=util.tomorrow(today=today), dry_run_param=True)

        return "status: {}, data: {}".format(response.status_code, str(response.data))
