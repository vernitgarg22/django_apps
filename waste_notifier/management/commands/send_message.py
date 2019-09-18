from django.core.management.base import BaseCommand, CommandError

from cod_utils.messaging.msg_handler import get_dpw_msg_handler


class Command(BaseCommand):
    help = """
        Use this to send a text message to a user, e.g.,
        python manage.py send_message '2125799232' 'This is a message to send to the user' """

    def add_arguments(self, parser):
        parser.add_argument('phone_number', type=str)
        parser.add_argument('message', type=str)
        parser.add_argument('--phone_sender', type=str, default=None)

    def handle(self, *args, **options):
        phone_number = options['phone_number']
        message = options['message']
        phone_sender = options['phone_sender']
        get_dpw_msg_handler().send_text(phone_number=phone_number, text=message, phone_sender=phone_sender)
        return "Sent message '{}' to phone_number {}".format(message, phone_number,)
