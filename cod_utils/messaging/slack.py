from django.conf import settings

from slackclient import SlackClient


class SlackMsgHandler():

    DRY_RUN = settings.DEBUG or settings.DRY_RUN

    def __init__(self):

        self.client = SlackClient(settings.AUTO_LOADED_DATA["SLACK_API_TOKEN"])
        self.ts = None

    def send(self, message, channel="#z_twilio"):
        """
        Slack a message to the City of Detroit #zzz slack channel
        """

        if SlackMsgHandler.DRY_RUN:
            return False

        result = self.client.api_call("chat.postMessage", channel=channel, text=message, timeout=60)

        self.ts = result.get('ts', None)
        return result.get('ok', False)

    def comment(self, message, channel="#z_twilio"):

        if SlackMsgHandler.DRY_RUN or not self.ts:
            return False

        result = self.client.api_call(
            "chat.postMessage",
            channel=channel,
            text=message,
            thread_ts=self.ts,
            timeout=60
        )

        return result.get('ok', False)

    def send_admin_alert(self, message, dry_run_param = False):
        """
        Send admins an alert.
        """

        if SlackMsgHandler.DRY_RUN or dry_run_param:
            return False    # pragma: no cover

        # REVIEW: use a better channel (e.g., #alerts-admin?)
        result = self.client.api_call("chat.postMessage", channel="#z_testing", text=message, timeout=60)

        self.ts = result.get('ts', None)
        return result.get('ok', False)


class SlackAlertProgressHandler():

    def __init__(self, description, item="messages"):

        self.slack_msg_handler = SlackMsgHandler()
        self.description = description
        self.item = item

    def slack_alerts_start(self):
        """
        Slack a message indicating that alerts are beginning to channel #z_twilio.
        """

        self.slack_msg_handler.send(message="Beginning {description}".format(description=self.description))

    def slack_alerts_update(self, msg_cnt = 0):
        """
        Slacks a progress update of alerts to channel #z_twilio.
        """

        message = "{msg_cnt} {item} sent".format(msg_cnt=msg_cnt, item=self.item)
        self.slack_msg_handler.comment(message=message)

    def slack_alerts_summary(self, summary):
        """
        Slacks a summary of alerts to channel #z_twilio.
        """

        # summary = format_slack_alerts_summary(content)
        self.slack_msg_handler.comment(message=summary)
