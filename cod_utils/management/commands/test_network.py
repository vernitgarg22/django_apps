import requests

from django.core.management.base import BaseCommand, CommandError

from cod_utils.messaging import SlackMsgHandler


class Command(BaseCommand):
    help = """Use this to look for network problems"""

    SERVERS = { 
        "apis.detroitmi.gov": "10.208.37.172",
    }

    @staticmethod
    def try_connect(server):

        try:
            response = requests.get("http://" + server)
            return response.ok
        except:
            return False

    def handle(self, *args, **options):

        domain_errors = []
        server_errors = []

        for domain, internal_ip in Command.SERVERS.items():

            if not Command.try_connect(domain):

                domain_errors.append(domain)

                if not Command.try_connect(internal_ip):

                    server_errors.append(internal_ip)

        error_msg = ""
        if domain_errors:
            error_msg = "The following domains are down: {}".format(domain_errors)
        if server_errors:
            error_msg = error_msg + "\nThe following servers are down: {}".format(server_errors)

        if error_msg:
            SlackMsgHandler().send(message=error_msg)
        else:
            print('No network problems detected')