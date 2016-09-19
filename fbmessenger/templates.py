from __future__ import absolute_import

from .quick_replies import QuickReplies


class BaseTemplate(object):
    def __init__(self, elements=None, quick_replies=None):
        if elements and not isinstance(elements, list):
            elements = [elements]
        self._elements = elements

        if quick_replies and not isinstance(quick_replies, QuickReplies):
            raise ValueError('quick_replies must be an instance of QuickReplies.')
        self.quick_replies = quick_replies

        self._d = {
            'attachment': {
                'type': 'template',
            },
        }

    @property
    def elements(self):
        if self._elements and len(self._elements) > 10:
            raise ValueError('You cannot have more than 10 elements in the template.')
        return self._elements

    def to_dict(self):
        if self.quick_replies:
            self._d['quick_replies'] = self.quick_replies.to_dict()

        return self._d


class GenericTemplate(BaseTemplate):

    def __init__(self, elements, quick_replies=None):
        self._elements = elements
        self.quick_replies = quick_replies
        super(GenericTemplate, self).__init__(self._elements, self.quick_replies)

    def to_dict(self):
        self._d['attachment']['payload'] = {
            'template_type': 'generic',
            'elements': [
                element.to_dict() for element in self.elements
            ]
        }
        return super(GenericTemplate, self).to_dict()


class ButtonTemplate(BaseTemplate):

    def __init__(self, text, buttons, quick_replies=None):
        self.text = text
        self.quick_replies = quick_replies

        if not isinstance(buttons, list):
            buttons = [buttons]
        self.buttons = buttons

        super(ButtonTemplate, self).__init__(None, self.quick_replies)

    def to_dict(self):
        self._d['attachment']['payload'] = {
            'template_type': 'button',
            'text': self.text,
            'buttons': [
                button.to_dict() for button in self.buttons
            ]
        }
        return super(ButtonTemplate, self).to_dict()


class ReceiptTemplate(BaseTemplate):

    def __init__(self, recipient_name, order_number, currency, payment_method,
                 elements, summary, order_url=None, timestamp=None,
                 address=None, adjustments=None, quick_replies=None):

        self._elements = elements
        self.recipient_name = recipient_name
        self.order_number = order_number
        self.currency = currency
        self.payment_method = payment_method
        self.summary = summary.to_dict()
        self.order_url = order_url
        self.timestamp = timestamp
        self.address = address
        self.adjustments = adjustments
        self.quick_replies = quick_replies

        super(ReceiptTemplate, self).__init__(self._elements, self.quick_replies)

    def to_dict(self):
        self._d['attachment']['payload'] = {
            'template_type': 'receipt',
            'recipient_name': self.recipient_name,
            'order_number': self.order_number,
            'order_url': self.order_url,
            'currency': self.currency,
            'timestamp': self.timestamp,
            'payment_method': self.payment_method,
            'elements': [
                element.to_dict() for element in self.elements
            ],
            'summary': self.summary
        }

        if self.address:
            self._d['attachment']['payload']['address'] = self.address.to_dict()

        if self.adjustments:
            self._d['attachment']['payload']['adjustments'] = [
                adjustment.to_dict() for adjustment in self.adjustments
            ]

        return super(ReceiptTemplate, self).to_dict()
