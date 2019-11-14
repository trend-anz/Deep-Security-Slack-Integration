import slack
import os
import json

SLACK_CHANNEL_NAME = os.getenv('SLACK_CHANNEL_NAME')
SLACK_API_TOKEN = os.getenv('SLACK_API_TOKEN')


class SlackClient:
    def __init__(self):
        self.sc = slack.WebClient(token=SLACK_API_TOKEN)
        self.channel_id = self._get_channel_id(SLACK_CHANNEL_NAME)

    def _get_channel_id(self, channel_name):
        get_channels = self.sc.api_call('channels.list')
        for channel in get_channels['channels']:
            if channel['name'] == channel_name:
                channel_id = channel['id']

                return channel_id

    def send_msg(self, msg):
        self.sc.chat_postMessage(channel=self.channel_id, text=msg, type='mrkdwn')


def _prettify_message(messages):
    msg = []

    for message in messages:
        for k, v in message.items():
            kv_pair = f'{k}: {v}'
            msg.append(kv_pair)

    joined_msg = '\n'.join(msg)
    return joined_msg


def lambda_handler(event, context):
    print('Received SNS notification. Payload will be printed below:')
    print(json.dumps(event))

    sc = SlackClient()

    for record in event['Records']:
        msg = record['Sns']['Message']

        load_msg = json.loads(msg)
        log_msg = json.dumps(load_msg)
        print('Extracted message. Payload will be printed below:')
        print(log_msg)

        dict_msg = json.loads(msg)
        pretty_msg = _prettify_message(dict_msg)
        sc.send_msg(pretty_msg)
        print(f'Message was sent to #{SLACK_CHANNEL_NAME} successfully')
