from __future__ import absolute_import

import logging

from .error_messages import CHARACTER_LIMIT_MESSAGE

logger = logging.getLogger(__name__)


class Text(object):
    def __init__(self, text, quick_replies=None):
        self.text = text
        self.quick_replies = quick_replies

    def to_dict(self):
        d = {
            'text': self.text
        }

        if self.quick_replies:
            d['quick_replies'] = self.quick_replies.to_dict()

        return d


class Button(object):
    BUTTON_TYPES = [
        'web_url',
        'postback',
        'phone_number',
        'account_link',
        'account_unlink',
        'element_share',
    ]

    WEBVIEW_HEIGHT_RATIOS = [
        'compact',
        'tall',
        'full',
    ]

    def __init__(self, button_type, title=None, url=None,
                 payload=None, webview_height_ratio=None,
                 messenger_extensions=None, fallback_url=None):

        if button_type not in self.BUTTON_TYPES:
            raise ValueError('Invalid button_type provided.')
        if webview_height_ratio and webview_height_ratio not in self.WEBVIEW_HEIGHT_RATIOS:
            raise ValueError('Invalid webview_height_ratio provided.')
        if title and len(title) > 20:
            logger.warning(CHARACTER_LIMIT_MESSAGE.format(field='Title',
                                                          maxsize=20))

        self.button_type = button_type
        self.title = title
        self.url = url
        self.payload = payload
        self.webview_height_ratio = webview_height_ratio
        self.messenger_extensions = messenger_extensions
        self.fallback_url = fallback_url

    def to_dict(self):
        d = {
            'type': self.button_type,
        }

        if self.title:
            d['title'] = self.title
        if self.url:
            d['url'] = self.url
        if self.payload:
            d['payload'] = self.payload
        if self.button_type == 'web_url':
            if self.webview_height_ratio:
                d['webview_height_ratio'] = self.webview_height_ratio
            if self.messenger_extensions:
                d['messenger_extensions'] = 'true'
            if self.fallback_url:
                d['fallback_url'] = self.fallback_url
        return d


class Element(object):
    """
    To be used with the generic template to create a carousel
    """

    def __init__(self, title, item_url=None, image_url=None,
                 subtitle=None, buttons=None, quantity=None,
                 price=None, currency=None):

        self.title = title
        self.item_url = item_url
        self.image_url = image_url
        self.subtitle = subtitle
        self.buttons = buttons
        self.quantity = quantity
        self.price = price
        self.currency = currency

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if len(title) > 80:
            logger.warning(CHARACTER_LIMIT_MESSAGE.format(field='Title',
                                                          maxsize=80))
        self._title = title

    @property
    def subtitle(self):
        return self._subtitle

    @subtitle.setter
    def subtitle(self, subtitle):
        if subtitle is not None and len(subtitle) > 80:
            logger.warning(CHARACTER_LIMIT_MESSAGE.format(field='Subtitle',
                                                          maxsize=80))
        self._subtitle = subtitle

    def to_dict(self):
        d = {
            'title': self.title,
        }
        if self.item_url:
            d['item_url'] = self.item_url
        if self.image_url:
            d['image_url'] = self.image_url
        if self.subtitle:
            d['subtitle'] = self.subtitle
        if self.quantity:
            d['quantity'] = self.quantity
        if self.price:
            d['price'] = self.price
        if self.currency:
            d['currency'] = self.currency
        if self.buttons:
            d['buttons'] = [
                button.to_dict() for button in self.buttons
            ]

        return d


class Adjustment(object):
    def __init__(self, name=None, amount=None):
        # Optional
        self.name = name
        self.amount = amount

    def to_dict(self):
        return {
            'name': self.name,
            'amount': self.amount
        }


class Address(object):
    def __init__(self, street_1, city, postal_code,
                 state, country, street_2=''):
        # Required
        self.street_1 = street_1
        self.city = city
        self.postal_code = postal_code
        self.state = state
        self.country = country
        # Optional
        self.street_2 = street_2

    def to_dict(self):
        return {
            'street_1': self.street_1,
            'street_2': self.street_2,
            'city': self.city,
            'postal_code': self.postal_code,
            'state': self.state,
            'country': self.country,
        }


class Summary(object):
    def __init__(self, total_cost, subtotal=None, shipping_cost=None, total_tax=None):
        # Required
        self.total_cost = total_cost
        # Optional
        self.subtotal = subtotal
        self.shipping_cost = shipping_cost
        self.total_tax = total_tax

    def to_dict(self):
        return {
            'subtotal': self.subtotal,
            'shipping_cost': self.shipping_cost,
            'total_tax': self.total_tax,
            'total_cost': self.total_cost
        }
