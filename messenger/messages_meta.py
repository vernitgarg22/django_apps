from cod_utils.messaging.slack import SlackAlertProgressHandler


class MessagesMeta():

    class NotificationMeta():

        def __init__(self, notification):

            self.notification = notification
            self.num_messages_sent = 0

        def update(self):

            self.num_messages_sent += 1
            return self.num_messages_sent

        def describe(self):

            messenger_message = self.notification.get_message_by_lang(lang=None)

            description = """
id:                 {id}
message:            {message}
geo layer url:      {geo_layer_url}
formatter:          {formatter}
num messages sent:  {num_messages_sent}
""".format(id=self.notification.id,
message=messenger_message.message, geo_layer_url=self.notification.geo_layer_url, formatter=self.notification.formatter, num_messages_sent=self.num_messages_sent)

            return description

    def __init__(self, client_name, day):

        self.client_name = client_name
        self.day = day
        self.notifications_meta = {}
        self.slack_handler = SlackAlertProgressHandler(description=self.client_name)

    @staticmethod
    def do_send_alerts_update(msg_cnt):
        return msg_cnt % 100 == 0

    def update(self, notification):
        """
        Updates the notification metadata for each message sent.
        """

        # Make sure this notification has metadata set up.
        if not self.notifications_meta.get(notification.id, None):

            notification_meta = MessagesMeta.NotificationMeta(notification=notification)
            self.notifications_meta[notification.id] = notification_meta

        # Update the metadata.
        msg_cnt = self.notifications_meta[notification.id].update()

        # Send out a slack update on our progress?
        if MessagesMeta.do_send_alerts_update(msg_cnt=msg_cnt):
            self.slack_handler.slack_alerts_update(msg_cnt=msg_cnt)

    def describe(self):

        description = """
client: {client_name}
day:    {day}

notifications:""".format(client_name=self.client_name, day=self.day)

        if self.notifications_meta:

            for notification_meta in self.notifications_meta.values():
                description += "\n" + notification_meta.describe()

        else:
            description += "  (No notifications sent)"

        return description
