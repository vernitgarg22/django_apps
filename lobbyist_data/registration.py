from datetime import datetime


class Registration:

    def __init__(self, date, address, city, state, zipcode, phone, reg_type_fed, reg_type_mi, reg_type_state_other, expend_1000, expend_250, attachment = None):
        self.date = datetime.strptime(date, '%Y-%m-%d')
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.phone = phone
        self.reg_type_fed = reg_type_fed
        self.reg_type_mi = reg_type_mi
        self.reg_type_state_other = reg_type_state_other
        self.expend_1000 = expend_1000
        self.expend_250 = expend_250
        self.attachment = attachment

    def __lt__(self, other):
         return self.date < other.date

    def __str__(self):
        return str(self.id) + ' attachment: ' + self.attachment

    def to_json(self):
        content = {
            "date": self.date,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "zipcode": self.zipcode,
            "phone": self.phone,
            "reg_type_fed": self.reg_type_fed,
            "reg_type_mi": self.reg_type_mi,
            "reg_type_state_other": self.reg_type_state_other,
            "expend_1000": self.expend_1000,
            "expend_250": self.expend_250,
        }
        if self.attachment != None:
            content["attachment"] = self.attachment.to_json()
        return content
