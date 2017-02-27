from .attachment import Attachment
from .client import Client
from .registration import Registration


class Lobbyist:

    def __init__(self, regid, name, date, attachment = None):
        self.regid = int(regid)
        self.name = name
        self.registrations = []
        self.clients = []
        self.add_registration(date, attachment)

    def add_registration(self, date, attachment = None):
        self.registrations.append(Registration(date, attachment))

    def add_client(self, client):
        self.clients.append(client)

    def registrations_json(self):
        content= []
        for registration in sorted(self.registrations):
            content.append(registration.to_json())
        return content

    def clients_json(self):
        content= []
        for client in sorted(self.clients):
            content.append(client.to_json())
        return content

    def to_json(self):
        return {
            "regid": self.regid,
            "name": self.name,
            "registrations": self.registrations_json(),
            "clients": self.clients_json()
        }

    def __lt__(self, other):
         return self.regid < other.regid

    def __str__(self):
        return 'regid: ' + str(self.regid) + ' - name: ' + str(self.name) + ' - num dates: ' + str(len(self.dates))
