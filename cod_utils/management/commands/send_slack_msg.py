from django.core.management.base import BaseCommand, CommandError

from cod_utils.messaging import SlackMsgHandler


class Command(BaseCommand):
    help = """
        Use this to slack a slack channel, e.g.,
        python manage.py send_slack_msg 'A job failed' """

    def add_arguments(self, parser):

        parser.add_argument('-c', '--channel', default="#z_twilio", type=str, help='Specify the slack channel to use')
        parser.add_argument('-m', '--message', default=None, type=str, help='The message to send')
        parser.add_argument('message', default=None, type=str, help='The message to send')

    def handle(self, *args, **options):

        channel = options['channel']
        message = options['message']

        SlackMsgHandler().send(message=message, channel=channel)
        return "Sent message '{}' to channel {}".format(message, channel)
