#!/usr/bin/env python

from waste_notifier.models import Subscriber
from waste_notifier.management.commands.send_message import Command


import pdb


pdb.set_trace()


subscribers = Subscriber.objects.filter(status = 'active').filter(address__isnull = True)

for subscriber in subscribers:

    cmd = Command()

    # opts = {
    #     'phone_number': subscriber.phone_number,
    #     'message': 'City of Detroit Public Works:  Please reply to this text message with your street address in order to update the schedule for your waste pickup reminders',
    #     'phone_sender': '3138007905'
    # }

    # cmd.handle(**opts)
