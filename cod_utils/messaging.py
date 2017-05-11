import json
import requests

from django.conf import settings


class SlackMsgHandler():

    WEBHOOK_URL = "https://hooks.slack.com/services/" + settings.AUTO_LOADED_DATA["SLACK_ZZZ_TOKEN"]
    DRY_RUN = settings.DEBUG or settings.DRY_RUN

    def send(self, message):     # pragma: no cover  TODO mock-patch this out so we can test it better
        """
        Slack a message to the City of Detroit #zzz slack channel
        """

        slack_data = { "text": message }
        if SlackMsgHandler.DRY_RUN:
            return False
        response = requests.post(
            SlackMsgHandler.WEBHOOK_URL, data=json.dumps(slack_data),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
            raise ValueError(
                'Request to slack returned {}, the response is:\n{}'.format(response.status_code, response.text)
            )
            return False
        else:
            return True