class Attachment:

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return str(self.id) + ' ' + self.name

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name
        }
