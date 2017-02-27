from .attachment import Attachment
from .client import Client
from .lobbyist import Lobbyist


class LobbyistData:

    def __init__(self):
        self.lobbyists = {}

    def add_lobbyist(self, regid, name, date, attachment = None):
            lobbyist = self.lobbyists.get(regid)
            if lobbyist:
                lobbyist.add_registration(date, attachment)
            else:
                lobbyist = Lobbyist(regid, name, date, attachment)
                self.lobbyists[regid] = lobbyist

    def add_client(self, regid, client):
        if self.lobbyists.get(regid):
            self.lobbyists[regid].add_client(client)

    def to_json(self):
        content = []
        for lobbyist in sorted(self.lobbyists.values()):
            content.append(lobbyist.to_json())
        return content
