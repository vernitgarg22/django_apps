from django.core.management.base import BaseCommand, CommandError

from cod_utils.messaging import MsgHandler


class Command(BaseCommand):
    help = """
        Use this to send a text message to a user, e.g.,
        python manage.py send_message '2125799232' 'This is a message to send to the user' """

    def add_arguments(self, parser):
        parser.add_argument('phone_number', type=str)
        parser.add_argument('message', type=str)

    def handle(self, *args, **options):
        phone_number = options['phone_number']
        message = options['message']
        MsgHandler().send_text(phone_number=phone_number, text=message)
        return "Sent message '{}' to phone_number {}".format(message, phone_number)