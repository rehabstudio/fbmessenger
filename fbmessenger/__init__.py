from __future__ import absolute_import
import abc
import logging

import requests

__version__ = '2.0.0'

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class MessengerClient(object):

    def __init__(self, page_access_token):
        self.page_access_token = page_access_token

    def get_user_data(self, entry):
        r = requests.get(
            'https://graph.facebook.com/v2.6/{sender}'.format(sender=entry['sender']['id']),
            params={
                'fields': 'first_name,last_name,profile_pic,locale,timezone,gender',
                'access_token': self.page_access_token
            }
        )
        return r.json()

    def send(self, payload, entry):
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

    def send_action(self, sender_action, entry):
        r = requests.post(
            'https://graph.facebook.com/v2.6/me/messages',
            params={
                'access_token': self.page_access_token
            },
            json={
                'recipient': {
                    'id': entry['sender']['id']
                },
                'sender_action': sender_action
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

    def set_thread_setting(self, data):
        r = requests.post(
            'https://graph.facebook.com/v2.6/me/thread_settings',
            params={
                'access_token': self.page_access_token
            },
            json=data
        )
        return r.json()

    def delete_get_started(self):  # pragma: no cover
        r = requests.delete(
            'https://graph.facebook.com/v2.6/me/thread_settings',
            params={
                'access_token': self.page_access_token
            },
            json={
                'setting_type': 'call_to_actions',
                'thread_state': 'new_thread'
            }
        )
        return r.json()

    def link_account(self, account_linking_token):
        r = requests.post(
            'https://graph.facebook.com/v2.6/me',
            params={
                'access_token': self.page_access_token,
                'fields': 'recipient',
                'account_linking_token': account_linking_token
            }
        )
        return r.json()

    def unlink_account(self, psid):
        r = requests.post(
            'https://graph.facebook.com/v2.6/me/unlink_accounts',
            params={
                'access_token': self.page_access_token
            },
            json={
                'psid': psid
            }
        )
        return r.json()


class BaseMessenger(object):
    __metaclass__ = abc.ABCMeta

    last_message = {}

    def __init__(self, page_access_token):
        self.page_access_token = page_access_token
        self.client = MessengerClient(self.page_access_token)

    @abc.abstractmethod
    def account_linking(self, message):
        """Method to handle `account_linking`"""

    @abc.abstractmethod
    def messages(self, message):
        """Method to handle `messages`"""

    @abc.abstractmethod
    def message_deliveries(self, message):
        """Method to handle `message_deliveries`"""

    @abc.abstractmethod
    def messaging_optins(self, message):
        """Method to handle `messaging_optins`"""

    @abc.abstractmethod
    def messaging_postbacks(self, message):
        """Method to handle `messaging_postbacks`"""

    @abc.abstractmethod
    def message_reads(self, message):
        """Method to handle `message_reads`"""

    def handle(self, payload):
        for entry in payload['entry']:
            for message in entry['messaging']:
                self.last_message = message
                if message.get('account_linking'):
                    return self.account_linking(message)
                elif message.get('delivery'):
                    return self.message_deliveries(message)
                elif message.get('message'):
                    return self.messages(message)
                elif message.get('optin'):
                    return self.messaging_optins(message)
                elif message.get('postback'):
                    return self.messaging_postbacks(message)
                elif message.get('read'):
                    return self.message_reads(message)

    def get_user(self):
        return self.client.get_user_data(self.last_message)

    def send(self, payload):
        return self.client.send(payload, self.last_message)

    def send_action(self, sender_action):
        return self.client.send_action(sender_action, self.last_message)

    def get_user_id(self):
        return self.last_message['sender']['id']

    def subscribe(self):
        return self.client.subscribe_app_to_page()

    def set_thread_setting(self, data):
        return self.client.set_thread_setting(data)

    def delete_get_started(self):
        return self.client.delete_get_started()

    def link_account(self, account_linking_token):
        return self.client.link_account(account_linking_token)

    def unlink_account(self, psid):
        return self.client.unlink_account(psid)
