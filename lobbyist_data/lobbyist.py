from .attachment import Attachment
from .registration import Registration


class Lobbyist:

    def __init__(self, regid, name, date, attachment = None):
        self.regid = regid
        self.name = name
        self.registrations = []
        self.add_registration(date, attachment)

    def add_registration(self, date, attachment = None):
        self.registrations.append(Registration(date, attachment))

    def to_json(self):
        return {
            "regid": self.regid,
            "name": self.name,
            "registrations": self.registrations_json()
        }

    def registrations_json(self):
        content= []
        for registration in sorted(self.registrations):
            content.append(registration.to_json())
        return content

    def __lt__(self, other):
         return self.name < other.name

    def __str__(self):
        return 'regid: ' + str(self.regid) + ' - name: ' + str(self.name) + ' - num dates: ' + str(len(self.dates))
