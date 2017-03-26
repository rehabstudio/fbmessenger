DEFAULT_LOCALE = 'default'

class GreetingText(object):
    def __init__(self, text, locale=None):
        if len(text) > 160:
            raise ValueError('Text cannot be longer 160 characters.')
        self.text = text
        self.locale = locale or DEFAULT_LOCALE

    def to_dict(self):
        return {
            'locale': self.locale,
            'text': self.text,
            }


class GetStartedButton(object):
    def __init__(self, payload):
        self.payload = payload

    def to_dict(self):
        return {
            'payload': self.payload,
            }


class PersistentMenuItem(object):
    ITEM_TYPES = [
        'nested',
        'web_url',
        'postback'
    ]

    def __init__(self, item_type, title, nested_items=None, url=None, payload=None):
        if item_type not in self.ITEM_TYPES:
            raise ValueError('Invalid item_type provided.')
        if len(title) > 30:
            raise ValueError('Title cannot be longer 30 characters.')
        if payload and len(payload) > 1000:
            raise ValueError('Payload cannot be longer 1000 characters.')
        if item_type == 'nested':
            if not nested_items:
                raise ValueError('`nested_items` must be supplied for `nested` type menu items.')
            if len(nested_items) > 5:
                raise ValueError('Cannot have more than 5 nested_items')
        if item_type == 'web_url' and url is None:
            raise ValueError('`url` must be supplied for `web_url` type menu items.')
        if item_type == 'postback' and payload is None:
            raise ValueError('`payload` must be supplied for `postback` type menu items.')

        self.item_type = item_type
        self.title = title
        self.nested_items = nested_items
        self.url = url
        self.payload = payload

    def to_dict(self):
        res = {
            'type': self.item_type,
            'title': self.title
        }

        if self.nested_items and self.item_type == 'nested':
            res['call_to_actions'] = [item.to_dict() for item in self.nested_items]

        if self.url and self.item_type == 'web_url':
            res['url'] = self.url

        if self.payload and self.item_type == 'postback':
            res['payload'] = self.payload
        return res


class PersistentMenu(object):
    def __init__(self, menu_items=None, locale=None, composer_input_disabled=None):
        if composer_input_disabled != False:
            if not menu_items:
                raise ValueError('You must supply at least one menu_item.')

            elif len(menu_items) > 3:
                raise ValueError('You cannot have more than 3 menu_items in top level.')

        self.menu_items = menu_items
        self.locale = locale or DEFAULT_LOCALE
        self.composer_input_disabled = composer_input_disabled

    def to_dict(self):
        res = {
            'locale': self.locale,
        }

        if self.menu_items:
            res['call_to_actions'] = [
                item.to_dict() for item in self.menu_items
            ]

        if self.composer_input_disabled is not None:
            res['composer_input_disabled'] = self.composer_input_disabled

        return res


class MessengerProfile(object):
    def __init__(self, greetings=None, get_started=None, persistent_menus=None):
        self.greetings = greetings
        self.get_started = get_started
        self.persistent_menus = persistent_menus

    def to_dict(self):
        res = {}

        if self.greetings:
            res['greeting'] = [
                item.to_dict() for item in self.greetings]

        if self.get_started:
            res['get_started'] = self.get_started.to_dict()

        if self.persistent_menus:
            res['persistent_menu'] = [
                item.to_dict() for item in self.persistent_menus]

        return res
