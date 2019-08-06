from datetime import date

from django.core.management.base import BaseCommand, CommandError

from elections.models import ElectionNotification, ElectionSubscriber

from cod_utils import util
from cod_utils.messaging import MsgHandler


def send_election_notifications(today, dry_run_param):
    """
    Send out any and all election notifications.
    """


    # TODO figure out what the return value should be


    # TODO Find out what the elections info number is
    elections_info_number = None


    notifications = ElectionNotification.objects.filter(day=today)
    if not notifications:
        return

    subscribers = ElectionSubscriber.objects.all()
    for subscriber in subscribers:

        for notification in notifications:

            message = None

            if notification.notification_type == 'reminder':

                # TODO create a city-wide reminder - add in precinct info, etc.

                message = notification.message

            else:

                # TODO check if subscriber is geofenced by this notification
                # TODO if subscriber is geofenced here, then create the notification

            # Send the message?
            if message:
                MsgHandler().send_text(phone_number=subscriber.phone_number, phone_sender=elections_info_number, text=message)


class Command(BaseCommand):
    help = """
        Use this to send out elections notifications, e.g.,
        python manage.py send_election_notifications
        python manage.py send_election_notifications --today=YYYYMMDD --dry_run=<yes|no>
        python manage.py send_election_notifications --today=20190730 --dry_run=no
        """

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
        elif not type(today) == date:
            raise CommandError("Invalid data type for today param")    # pragma: no cover (should never get here)

        dry_run_param = dry_run_param == "yes"

        # response = views.send_notifications(date=util.tomorrow(today=today), dry_run_param=dry_run_param)

        return json.dumps({ "status": 200, "data": OrderedDict(response) })
