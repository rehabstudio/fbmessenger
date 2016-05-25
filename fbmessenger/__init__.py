from __future__ import absolute_import
import logging

import requests

__version__ = '0.1.0'

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class MessengerClient(object):

    def __init__(self, page_access_token):
        self.page_access_token = page_access_token

    def get_user_data(self, entry):
        r = requests.get(
            'https://graph.facebook.com/v2.6/{sender}'.format(sender=entry['sender']['id']),
            params={
                'fields': 'first_name,last_name,profile_pic',
                'access_token': self.page_access_token
            }
        )
        return r.json()

    def send_data(self, payload, entry):
        r = requests.post(
            'https://graph.facebook.com/v2.6/me/messages',
            params={
                'access_token': self.page_access_token
            },
            json={
                'recipient': {
                    'id': entry['sender']['id']
                },
                'message': payload
            }
        )
        return r.json()

    def subscribe_app_to_page(self):
        r = requests.post(
            'https://graph.facebook.com/v2.6/me/subscribed_apps',
            params={
                'access_token': self.page_access_token
            }
        )
        return r.json()

    def set_welcome_message(self, payload=None):
        actions = []
        if payload:
            actions = [{
                'message': payload
            }]
        r = requests.post(
            'https://graph.facebook.com/v2.6/me/thread_settings',
            params={
                'access_token': self.page_access_token
            },
            json={
                'setting_type': 'call_to_actions',
                'thread_state': 'new_thread',
                'call_to_actions': actions
            }
        )
        return r.json()


class BaseMessenger(object):

    last_message = {}

    def __init__(self, verify_token, page_access_token):
        self.verify_token = verify_token
        self.page_access_token = page_access_token
        self.client = MessengerClient(self.page_access_token)

    def verify(self, verify_token, challenge):
        if (verify_token == self.verify_token):
            return challenge
        raise ValueError('FB_VERIFY_TOKEN does not match.')

    def messages(self, message):
        raise NotImplementedError('`messages` is not implemented.')

    def message_deliveries(self, message):
        raise NotImplementedError('`message_deliveries` is not implemented.')

    def messaging_postbacks(self, message):
        raise NotImplementedError('`messaging_postbacks` is not implemented.')

    def messaging_optins(self, message):
        raise NotImplementedError('`messaging_optins` is not implemented.')

    def handle(self, payload):
        for entry in payload['entry']:
            for message in entry['messaging']:
                self.last_message = message
                if message.get('message'):
                    try:
                        return self.messages(message)
                    except NotImplementedError:
                        logger.error('messages is not implemented.')
                elif message.get('delivery'):
                    try:
                        return self.message_deliveries(message)
                    except NotImplementedError:
                        logger.error('message_deliveries is not implemented.')
                elif message.get('postback'):
                    try:
                        return self.messaging_postbacks(message)
                    except NotImplementedError:
                        logger.error('messaging_postbacks is not implemented.')
                elif message.get('optin'):
                    try:
                        return self.messaging_optins(message)
                    except NotImplementedError:
                        logger.error('messaging_optins is not implemented.')

    def get_user(self):
        return self.client.get_user_data(self.last_message)

    def send(self, payload):
        return self.client.send_data(payload, self.last_message)

    def get_user_id(self):
        return self.last_message['sender']['id']

    def subscribe(self):
        return self.client.subscribe_app_to_page()

    def set_welcome_message(self):
        return self.client.set_welcome_message()
