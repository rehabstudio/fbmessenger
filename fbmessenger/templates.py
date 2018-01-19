from __future__ import absolute_import

import collections
from .quick_replies import QuickReplies


class BaseTemplate(object):
    TEMPLATE_TYPE = 'base'

    def __init__(self, quick_replies=None):
        if quick_replies and not isinstance(quick_replies, QuickReplies):
            raise ValueError('quick_replies must be an instance of QuickReplies.')
        self.quick_replies = quick_replies

        self._d = {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': self.TEMPLATE_TYPE,
                },
            },
        }

    def to_dict(self):
        if self.quick_replies:
            self._d['quick_replies'] = self.quick_replies.to_dict()

        return self._d


class ElementMixin(object):
    MIN_ELEMENTS = 0
    MAX_ELEMENTS = 0

    def __init__(self, elements=None, *args, **kwargs):
        self.elements = elements

        super(ElementMixin, self).__init__(*args, **kwargs)

    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, elements):
        if elements:
            if isinstance(elements, collections.Iterable):
                elements = list(elements)
            else:
                elements = [elements]

        self._elements = elements

    def to_dict(self):
        if self.MIN_ELEMENTS and (not self.elements or len(self.elements) < self.MIN_ELEMENTS):
            raise ValueError('At least {} elements are required.'.format(self.MIN_ELEMENTS))

        if self.elements:
            if len(self.elements) > self.MAX_ELEMENTS:
                raise ValueError('You cannot have more than {} elements in the template.'.format(self.MAX_ELEMENTS))

            self._d['attachment']['payload']['elements'] = [
                element.to_dict() for element in self.elements
            ]

        return super(ElementMixin, self).to_dict()


class ButtonMixin(object):
    MIN_BUTTONS = 0
    MAX_BUTTONS = 0

    def __init__(self, buttons=None, *args, **kwargs):
        self.buttons = buttons

        super(ButtonMixin, self).__init__(*args, **kwargs)

    @property
    def buttons(self):
        return self._buttons

    @buttons.setter
    def buttons(self, buttons):
        if buttons:
            if isinstance(buttons, collections.Iterable):
                buttons = list(buttons)
            else:
                buttons = [buttons]

        self._buttons = buttons

    def to_dict(self):
        if self.MIN_BUTTONS and (not self.buttons or len(self.buttons) < self.MIN_BUTTONS):
            raise ValueError('At least {} buttons are required.'.format(self.MIN_BUTTONS))

        if self.buttons:
            if len(self.buttons) > self.MAX_BUTTONS:
                raise ValueError('You cannot have more than {} buttons in the template.'.format(self.MAX_BUTTONS))

            self._d['attachment']['payload']['buttons'] = [
                button.to_dict() for button in self.buttons
            ]

        return super(ButtonMixin, self).to_dict()


class SharableMixin(object):
    def __init__(self, sharable=False, *args, **kwargs):
        self.sharable = bool(sharable)

        super(SharableMixin, self).__init__(*args, **kwargs)

    def to_dict(self):
        self._d['attachment']['payload']['sharable'] = self.sharable

        return super(SharableMixin, self).to_dict()


class GenericTemplate(ElementMixin, SharableMixin, BaseTemplate):
    TEMPLATE_TYPE = 'generic'

    MIN_ELEMENTS = 1
    MAX_ELEMENTS = 10

    def __init__(self, elements, quick_replies=None, image_aspect_ratio=None, **kwargs):
        self.image_aspect_ratio = image_aspect_ratio

        super(GenericTemplate, self).__init__(
            elements=elements,
            quick_replies=quick_replies,
            **kwargs
            )

    def to_dict(self):
        if self.image_aspect_ratio:
            self._d['attachment']['payload']['image_aspect_ratio'] = self.image_aspect_ratio

        return super(GenericTemplate, self).to_dict()


class MediaTemplate(BaseTemplate):
    TEMPLATE_TYPE = 'media'

    VALID_MEDIA_TYPES = ('image', 'video')

    def __init__(self, media, buttons=None):
        if media.attachment_type not in self.VALID_MEDIA_TYPES:
            raise ValueError('Only image and video types are supported')
        self.media = media
        self.buttons = buttons
        super(MediaTemplate, self).__init__()

    def to_dict(self):
        # Media's dict has an extra layer of structure we don't need
        media_dict = self.media.to_dict()
        element = media_dict['attachment']['payload']
        element['media_type'] = self.media.attachment_type
        if self.buttons:
            element['buttons'] = [b.to_dict() for b in self.buttons]
        self._d['attachment']['payload']['elements'] = [element]
        return super(MediaTemplate, self).to_dict()



class ButtonTemplate(ButtonMixin, BaseTemplate):
    TEMPLATE_TYPE = 'button'

    MIN_BUTTONS = 1
    MAX_BUTTONS = 3

    def __init__(self, text, buttons, quick_replies=None, **kwargs):
        self.text = text

        super(ButtonTemplate, self).__init__(
            buttons=buttons,
            quick_replies=quick_replies,
            **kwargs
            )

    def to_dict(self):
        self._d['attachment']['payload']['text'] = self.text
        return super(ButtonTemplate, self).to_dict()


class ListTemplate(ButtonMixin, ElementMixin, BaseTemplate):
    TEMPLATE_TYPE = 'list'

    MIN_BUTTONS = 0
    MAX_BUTTONS = 1

    MIN_ELEMENTS = 2
    MAX_ELEMENTS = 4

    def __init__(self, elements, top_element_style=None, **kwargs):
        self.top_element_style = top_element_style

        super(ListTemplate, self).__init__(elements=elements, **kwargs)

    def to_dict(self):
        if self.top_element_style:
            self._d['attachment']['payload']['top_element_style'] = self.top_element_style

        return super(ListTemplate, self).to_dict()


class ReceiptTemplate(ElementMixin, SharableMixin, BaseTemplate):
    TEMPLATE_TYPE = 'receipt'

    MIN_ELEMENTS = 0
    MAX_ELEMENTS = 100

    def __init__(self, recipient_name, order_number, currency, payment_method,
                 elements, summary, order_url=None, timestamp=None,
                 address=None, adjustments=None, quick_replies=None,
                 **kwargs):

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

        super(ReceiptTemplate, self).__init__(
            elements=elements,
            quick_replies=quick_replies,
            **kwargs
            )

    def to_dict(self):
        payload = {
            'recipient_name': self.recipient_name,
            'order_number': self.order_number,
            'order_url': self.order_url,
            'currency': self.currency,
            'timestamp': self.timestamp,
            'payment_method': self.payment_method,
            'summary': self.summary
        }

        if self.address:
            payload['address'] = self.address.to_dict()

        if self.adjustments:
            payload['adjustments'] = [
                adjustment.to_dict() for adjustment in self.adjustments
            ]

        self._d['attachment']['payload'].update(payload)

        return super(ReceiptTemplate, self).to_dict()
