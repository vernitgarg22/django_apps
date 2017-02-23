from datetime import datetime


class Registration:

    def __init__(self, date, attachment = None):
        self.date = datetime.strptime(date, '%Y-%m-%d')
        self.attachment = attachment

    def __lt__(self, other):
         return self.date < other.date

    def __str__(self):
        return str(self.id) + ' attachment: ' + self.attachment

    def to_json(self):
        content = {
            "date": self.date
        }
        if self.attachment != None:
            content["attachment"] = self.attachment.to_json()
        return content
