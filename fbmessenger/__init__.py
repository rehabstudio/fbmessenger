from __future__ import absolute_import
import abc
import logging

import requests

__version__ = '5.0.0'

logger = logging.getLogger(__name__)


class MessengerClient(object):

    # https://developers.facebook.com/docs/messenger-platform/send-messages#send_api_basics
    MESSAGING_TYPES = {
        'RESPONSE',
        'UPDATE',
        'MESSAGE_TAG',
        'NON_PROMOTIONAL_SUBSCRIPTION'
    }

    def __init__(self, page_access_token):
        self.page_access_token = page_access_token
        self.session = requests.Session()

    def get_user_data(self, entry):
        r = self.session.get(
            'https://graph.facebook.com/v2.11/{sender}'.format(sender=entry['sender']['id']),
            params={
                'fields': 'first_name,last_name,profile_pic,locale,timezone,gender',
                'access_token': self.page_access_token
            }
        )
        return r.json()

    def send(self, payload, entry, messaging_type):
        if messaging_type not in self.MESSAGING_TYPES:
            raise ValueError(
                '`{}` is not a valid `messaging_type`'.format(messaging_type))
        r = self.session.post(
            'https://graph.facebook.com/v2.11/me/messages',
            params={
                'access_token': self.page_access_token
            },
            json={
                'messaging_type': messaging_type,
                'recipient': {
                    'id': entry['sender']['id']
                },
                'message': payload
            }
        )
        return r.json()

    def send_action(self, sender_action, entry):
        r = self.session.post(
            'https://graph.facebook.com/v2.11/me/messages',
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
        r = self.session.post(
            'https://graph.facebook.com/v2.11/me/subscribed_apps',
            params={
                'access_token': self.page_access_token
            }
        )
        return r.json()

    def set_messenger_profile(self, data):
        r = self.session.post(
            'https://graph.facebook.com/v2.11/me/messenger_profile',
            params={
                'access_token': self.page_access_token
            },
            json=data
        )
        return r.json()

    def delete_get_started(self):
        r = self.session.delete(
            'https://graph.facebook.com/v2.11/me/messenger_profile',
            params={
                'access_token': self.page_access_token
            },
            json={
                'fields':[
                    'get_started'
                ],
            }
        )
        return r.json()

    def delete_persistent_menu(self):
        r = self.session.delete(
            'https://graph.facebook.com/v2.11/me/messenger_profile',
            params={
                'access_token': self.page_access_token
            },
            json={
                'fields':[
                    'persistent_menu'
                ],
            }
        )
        return r.json()

    def link_account(self, account_linking_token):
        r = self.session.post(
            'https://graph.facebook.com/v2.11/me',
            params={
                'access_token': self.page_access_token,
                'fields': 'recipient',
                'account_linking_token': account_linking_token
            }
        )
        return r.json()

    def unlink_account(self, psid):
        r = self.session.post(
            'https://graph.facebook.com/v2.11/me/unlink_accounts',
            params={
                'access_token': self.page_access_token
            },
            json={
                'psid': psid
            }
        )
        return r.json()

    def update_whitelisted_domains(self, domains):
        if not isinstance(domains, list):
            domains = [domains]
        r = self.session.post(
            'https://graph.facebook.com/v2.11/me/messenger_profile',
            params={
                'access_token': self.page_access_token
            },
            json={
                'whitelisted_domains': domains
            }
        )
        return r.json()

    def remove_whitelisted_domains(self):
        r = self.session.delete(
            'https://graph.facebook.com/v2.11/me/messenger_profile',
            params={
                'access_token': self.page_access_token
            },
            json={
                'fields':[
                    'whitelisted_domains'
                ],
            }
        )
        return r.json()

    def upload_attachment(self, attachment):
        if not attachment.url:
            raise ValueError('Attachment must have `url` specified')
        if attachment.quick_replies:
            raise ValueError('Attachment may not have `quick_replies`')
        r = self.session.post(
            'https://graph.facebook.com/v2.11/me/message_attachments',
            params={
                'access_token': self.page_access_token
            },
            json={
                'message':  attachment.to_dict()
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
    def message(self, message):
        """Method to handle `messages`"""

    @abc.abstractmethod
    def delivery(self, message):
        """Method to handle `message_deliveries`"""

    @abc.abstractmethod
    def optin(self, message):
        """Method to handle `messaging_optins`"""

    @abc.abstractmethod
    def postback(self, message):
        """Method to handle `messaging_postbacks`"""

    @abc.abstractmethod
    def read(self, message):
        """Method to handle `message_reads`"""

    def handle(self, payload):
        for entry in payload['entry']:
            for message in entry['messaging']:
                self.last_message = message
                if message.get('account_linking'):
                    return self.account_linking(message)
                elif message.get('delivery'):
                    return self.delivery(message)
                elif message.get('message'):
                    return self.message(message)
                elif message.get('optin'):
                    return self.optin(message)
                elif message.get('postback'):
                    return self.postback(message)
                elif message.get('read'):
                    return self.read(message)

    def get_user(self):
        return self.client.get_user_data(self.last_message)

    def send(self, payload, messaging_type):
        return self.client.send(payload, self.last_message, messaging_type)

    def send_action(self, sender_action):
        return self.client.send_action(sender_action, self.last_message)

    def get_user_id(self):
        return self.last_message['sender']['id']

    def subscribe_app_to_page(self):
        return self.client.subscribe_app_to_page()

    def set_messenger_profile(self, data):
        return self.client.set_messenger_profile(data)

    def delete_get_started(self):
        return self.client.delete_get_started()

    def link_account(self, account_linking_token):
        return self.client.link_account(account_linking_token)

    def unlink_account(self, psid):
        return self.client.unlink_account(psid)

    def add_whitelisted_domains(self, domains):
        return self.client.update_whitelisted_domains(domains)

    def remove_whitelisted_domains(self):
        return self.client.remove_whitelisted_domains()

    def upload_attachment(self, attachment):
        return self.client.upload_attachment(attachment)
