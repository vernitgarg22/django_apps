from datetime import datetime


class Client:

    def __init__(self, name, address, city, state, zipcode, phone, start_date, end_date = None):
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.phone = phone
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date != None else None

    def to_json(self):
        return {
            "name": self.name,
            "start_date": self.start_date
        }

    def __lt__(self, other):
         return self.name < other.name

    def __str__(self):
        return self.name
