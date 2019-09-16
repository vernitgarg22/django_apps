from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError

from messenger.models import MessengerNotification


class Command(BaseCommand):
    help = """
        Use this to verify that the messenger app is in a valid state, e.g.,
        python manage.py validate_messenger
        """

    def handle(self, *args, **options):

        notifications = MessengerNotification.objects.all()
        for notification in notifications:

            try:
                notification.validate()
            except ValidationError as err:

                self.stdout.write("Notification {name} is invalid: {msg}".format(name=str(notification), msg=str(err.messages[0])))

                # REVIEW also slack something?
