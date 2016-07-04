class GreetingText(object):
    def __init__(self, text):
        if len(text) > 160:
            raise ValueError('Text cannot be longer 160 characters.')
        self.text = text

    def to_dict(self):
        return {
            'setting_type': 'greeting',
            'greeting': {
                'text': self.text
            }
        }


class GetStartedButton(object):
    def __init__(self, payload):
        self.payload = payload

    def to_dict(self):
        return {
            'setting_type': 'call_to_actions',
            'thread_state': 'new_thread',
            'call_to_actions': [
                {
                    'payload': self.payload
                }
            ]
        }


class PersistentMenuItem(object):
    ITEM_TYPES = [
        'web_url',
        'postback'
    ]

    def __init__(self, item_type, title, url=None, payload=None):
        if item_type not in self.ITEM_TYPES:
            raise ValueError('Invalid item_type provided.')
        if len(title) > 30:
            raise ValueError('Title cannot be longer 30 characters.')
        if payload and len(payload) > 1000:
            raise ValueError('Payload cannot be longer 1000 characters.')
        if item_type == 'web_url' and url is None:
            raise ValueError('`url` must be supplied for `web_url` type menu items.')
        if item_type == 'postback' and payload is None:
            raise ValueError('`postback` must be supplied for `payload` type menu items.')

        self.item_type = item_type
        self.title = title
        self.url = url
        self.payload = payload

    def to_dict(self):
        res = {
            'type': self.item_type,
            'title': self.title
        }

        if self.url and self.item_type == 'web_url':
            res['url'] = self.url

        if self.payload and self.item_type == 'postback':
            res['payload'] = self.payload
        return res


class PersistentMenu(object):
    def __init__(self, menu_items):
        if len(menu_items) > 5:
            raise ValueError('You cannot have more than 5 menu_items.')
        self.menu_items = menu_items

    def to_dict(self):
        return {
            'setting_type': 'call_to_actions',
            'thread_state': 'existing_thread',
            'call_to_actions': [
                item.to_dict() for item in self.menu_items
            ]
        }
