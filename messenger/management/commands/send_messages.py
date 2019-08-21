from datetime import date
import re

from django.core.management.base import BaseCommand, CommandError

from messenger.util import send_messages


class Command(BaseCommand):
    help = """
        Use this to send out messages (reminders, alerts, etc.), e.g.,
        python manage.py send_messages
        python manage.py send_messages --today=YYYYMMDD --dry_run=<yes|no>
        python manage.py send_messages --today=20190730 --dry_run=no
        """

    def add_arguments(self, parser):
        parser.add_argument('client', help='Name of client whose messages should be sent')
        parser.add_argument('--today', default=date.today(), help="Date value to treat as today. Format=YYYYMMDD")
        parser.add_argument('--dry_run', default='no', help="Pass 'yes' to do a dry run")

    def handle(self, *args, **options):

        # Validate and parse our command-line params
        client_name = options['client']
        today = options['today']
        dry_run_param = options['dry_run']

        if dry_run_param not in ['yes', 'no']:
            raise CommandError("--dry_run must be 'yes' or 'no'")

        if not type(today) == str or not re.fullmatch(r'^\d{8}$', today):
            raise CommandError("Date format for 'today' must be YYYYMMDD")

        today = date(int(today[0:4]), int(today[4:6]), int(today[6:8]))

        dry_run_param = dry_run_param == "yes"

        messages_meta = send_messages(client_name, day=today, dry_run_param=dry_run_param)

        print(messages_meta.describe())
