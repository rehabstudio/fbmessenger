class BaseTemplate(object):
    def __init__(self, elements):
        if not isinstance(elements, list):
            elements = [elements]
        self._elements = elements

    @property
    def elements(self):
        if len(self._elements) > 10:
            raise ValueError('You cannot have more than 10 elements in the template.')
        return self._elements


class GenericTemplate(BaseTemplate):

    def __init__(self, elements):
        self._elements = elements
        super(GenericTemplate, self).__init__(self._elements)

    def to_dict(self):
        return {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'elements': [
                        element.to_dict() for element in self.elements
                    ]
                }
            },
        }


class ButtonTemplate(object):

    def __init__(self, text, buttons):
        self.text = text

        if not isinstance(buttons, list):
            buttons = [buttons]
        self.buttons = buttons

    def to_dict(self):
        return {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'button',
                    'text': self.text,
                    'buttons': [
                        button.to_dict() for button in self.buttons
                    ]
                }
            }
        }


class ReceiptTemplate(BaseTemplate):

    def __init__(self, recipient_name, order_number, currency, payment_method,
                 elements, summary, order_url=None, timestamp=None,
                 address=None, adjustments=None):

        self._elements = elements
        self.recipient_name = recipient_name
        self.order_number = order_number
        self.currency = currency
        self.payment_method = payment_method
        self.summary = summary.to_dict()
        self.order_url = order_url
        self.timestamp = timestamp
        self.address = {} if address is None else address.to_dict()
        self.adjustments = [] if adjustments is None else adjustments

        super(ReceiptTemplate, self).__init__(self._elements)

    def to_dict(self):
        return {
            'attachment': {
                'type': 'template',
                'payload': {
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
                    'adjustments': [
                        adjustment.to_dict() for adjustment in self.adjustments
                    ],
                    'address': self.address,
                    'summary': self.summary
                }
            },
        }
