import pytest

from fbmessenger import attachments
from fbmessenger import elements
from fbmessenger import templates
from fbmessenger import quick_replies


class TestTemplates:

    def test_button_template_with_single_button(self):
        btn = elements.Button(button_type='web_url', title='Web button', url='http://facebook.com')
        res = templates.ButtonTemplate(
            text='Button template',
            buttons=btn
        )
        expected = {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'button',
                    'text': 'Button template',
                    'buttons': [
                        {
                            'type': 'web_url',
                            'title': 'Web button',
                            'url': 'http://facebook.com'
                        }
                    ]
                }
            }
        }
        assert expected == res.to_dict()

    def test_button_template_with_multiple_buttons(self):
        btn = elements.Button(button_type='web_url', title='Web button', url='http://facebook.com')
        btn2 = elements.Button(button_type='postback', title='Postback button', payload='payload')
        res = templates.ButtonTemplate(
            text='Button template',
            buttons=[btn, btn2]
        )
        expected = {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'button',
                    'text': 'Button template',
                    'buttons': [
                        {
                            'type': 'web_url',
                            'title': 'Web button',
                            'url': 'http://facebook.com'
                        },
                        {
                            'type': 'postback',
                            'title': 'Postback button',
                            'payload': 'payload'
                        }
                    ]
                }
            }
        }
        assert expected == res.to_dict()

    def test_button_template_with_too_many_buttons(self):
        btn = elements.Button(button_type='web_url', title='Web button', url='http://facebook.com')
        with pytest.raises(ValueError) as err:
            res = templates.ButtonTemplate(
                text='Button template',
                buttons=[btn]*4,
            )
            res.to_dict()
        assert str(err.value) == 'You cannot have more than 3 buttons in the template.'

    def test_button_template_with_no_buttons(self):
        with pytest.raises(ValueError) as err:
            res = templates.ButtonTemplate(
                text='Button template',
                buttons=[],
            )
            res.to_dict()
        assert str(err.value) == 'At least 1 buttons are required.'

    def test_generic_template(self):
        btn = elements.Button(
            button_type='web_url',
            title='Web button',
            url='http://facebook.com'
        )
        elems = elements.Element(
            title='Element',
            item_url='http://facebook.com',
            image_url='http://facebook.com/image.jpg',
            subtitle='Subtitle',
            buttons=[
                btn
            ]
        )
        res = templates.GenericTemplate(
            elements=[elems] * 2,
            image_aspect_ratio='square',
            sharable=True,
            )
        expected = {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'sharable': True,
                    'image_aspect_ratio': 'square',
                    'elements': [
                        {
                            'title': 'Element',
                            'item_url': 'http://facebook.com',
                            'image_url': 'http://facebook.com/image.jpg',
                            'subtitle': 'Subtitle',
                            'buttons': [
                                {
                                    'type': 'web_url',
                                    'title': 'Web button',
                                    'url': 'http://facebook.com'
                                }
                            ]
                        },
                        {
                            'title': 'Element',
                            'item_url': 'http://facebook.com',
                            'image_url': 'http://facebook.com/image.jpg',
                            'subtitle': 'Subtitle',
                            'buttons': [
                                {
                                    'type': 'web_url',
                                    'title': 'Web button',
                                    'url': 'http://facebook.com'
                                }
                            ]
                        }
                    ]
                }
            }
        }
        assert expected == res.to_dict()

    def test_generic_template_with_single_element(self):
        btn = elements.Button(
            button_type='web_url',
            title='Web button',
            url='http://facebook.com'
        )
        elems = elements.Element(
            title='Element',
            item_url='http://facebook.com',
            image_url='http://facebook.com/image.jpg',
            subtitle='Subtitle',
            buttons=[
                btn
            ]
        )
        res = templates.GenericTemplate(elements=elems)
        expected = {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'sharable': False,
                    'elements': [
                        {
                            'title': 'Element',
                            'item_url': 'http://facebook.com',
                            'image_url': 'http://facebook.com/image.jpg',
                            'subtitle': 'Subtitle',
                            'buttons': [
                                {
                                    'type': 'web_url',
                                    'title': 'Web button',
                                    'url': 'http://facebook.com'
                                }
                            ]
                        }
                    ]
                }
            }
        }
        assert expected == res.to_dict()

    def test_generic_template_with_quick_replies(self):
        btn = elements.Button(
            button_type='web_url',
            title='Web button',
            url='http://facebook.com'
        )
        elems = elements.Element(
            title='Element',
            item_url='http://facebook.com',
            image_url='http://facebook.com/image.jpg',
            subtitle='Subtitle',
            buttons=[
                btn
            ]
        )
        qr = quick_replies.QuickReply(title='QR', payload='QR payload')
        qrs = quick_replies.QuickReplies(quick_replies=[qr] * 2)
        res = templates.GenericTemplate(
            elements=[elems],
            quick_replies=qrs
        )
        expected = {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'sharable': False,
                    'elements': [
                        {
                            'title': 'Element',
                            'item_url': 'http://facebook.com',
                            'image_url': 'http://facebook.com/image.jpg',
                            'subtitle': 'Subtitle',
                            'buttons': [
                                {
                                    'type': 'web_url',
                                    'title': 'Web button',
                                    'url': 'http://facebook.com'
                                }
                            ]
                        }
                    ],
                },
            },
            'quick_replies': [
                {
                    'content_type': 'text',
                    'title': 'QR',
                    'payload': 'QR payload'
                },
                {
                    'content_type': 'text',
                    'title': 'QR',
                    'payload': 'QR payload'
                },
            ],
        }
        assert expected == res.to_dict()

    def test_template_with_too_many_elements(self):
        btn = elements.Button(button_type='web_url', title='Web button', url='http://facebook.com')
        elem = elements.Element(
            title='Element',
            item_url='http://facebook.com',
            image_url='http://facebook.com/image.jpg',
            subtitle='Subtitle',
            buttons=[
                btn
            ]
        )
        elem_list = [elem] * 11
        with pytest.raises(ValueError) as err:
            res = templates.GenericTemplate(elements=elem_list)
            res.to_dict()
        assert str(err.value) == 'You cannot have more than 10 elements in the template.'

    def test_generic_template_with_no_elements(self):
        with pytest.raises(ValueError) as err:
            res = templates.GenericTemplate(elements=[])
            res.to_dict()
        assert str(err.value) == 'At least 1 elements are required.'

    def test_template_with_invalid_quick_replies(self):
        with pytest.raises(ValueError) as err:
            templates.GenericTemplate(elements=None, quick_replies='wrong')
        assert str(err.value) == 'quick_replies must be an instance of QuickReplies.'

    def test_receipt_template(self):
        element = elements.Element(
            title='Classic White T-Shirt',
            subtitle='100% Soft and Luxurious Cotton',
            quantity=2,
            price=50,
            currency='USD',
            image_url='http://petersapparel.parseapp.com/img/whiteshirt.png',
        )
        adjustment1 = elements.Adjustment(name='New Customer Discount', amount=20)
        adjustment2 = elements.Adjustment(name='$10 Off Coupon', amount=10)
        address = elements.Address(
            street_1='1 Hacker Way',
            city='Menlo Park',
            postal_code='94025',
            state='CA',
            country='US'
        )
        summary = elements.Summary(
            subtotal=75.00,
            shipping_cost=4.95,
            total_tax=6.19,
            total_cost=56.14
        )
        res = templates.ReceiptTemplate(
            recipient_name='Stephane Crozatier',
            order_number='12345678902',
            currency='USD',
            payment_method='Visa 2345',
            order_url='http://petersapparel.parseapp.com/order?order_id=123456',
            timestamp='1428444852',
            address=address,
            summary=summary,
            adjustments=[adjustment1, adjustment2],
            elements=[element]
        )
        expected = {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'receipt',
                    'sharable': False,
                    'recipient_name': 'Stephane Crozatier',
                    'order_number': '12345678902',
                    'currency': 'USD',
                    'payment_method': 'Visa 2345',
                    'order_url': 'http://petersapparel.parseapp.com/order?order_id=123456',
                    'timestamp': '1428444852',
                    'elements': [
                        {
                            'title': 'Classic White T-Shirt',
                            'subtitle': '100% Soft and Luxurious Cotton',
                            'quantity': 2,
                            'price': 50,
                            'currency': 'USD',
                            'image_url': 'http://petersapparel.parseapp.com/img/whiteshirt.png'
                        }
                    ],
                    'address': {
                        'street_1': '1 Hacker Way',
                        'street_2': '',
                        'city': 'Menlo Park',
                        'postal_code': '94025',
                        'state': 'CA',
                        'country': 'US'
                    },
                    'summary': {
                        'subtotal': 75.00,
                        'shipping_cost': 4.95,
                        'total_tax': 6.19,
                        'total_cost': 56.14
                    },
                    'adjustments': [
                        {
                            'name': 'New Customer Discount',
                            'amount': 20
                        },
                        {
                            'name': '$10 Off Coupon',
                            'amount': 10
                        }
                    ]
                }
            }
        }
        assert expected == res.to_dict()

    def test_list_template(self):
        btn = elements.Button(
            button_type='web_url',
            title='Web button',
            url='http://facebook.com'
        )
        elems = elements.Element(
            title='Element',
            image_url='http://facebook.com/image.jpg',
            subtitle='Subtitle',
            buttons=[
                btn
            ]
        )
        res = templates.ListTemplate(
            elements=[elems] * 2,
            buttons=[btn],
            top_element_style='large',
            )
        expected = {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'list',
                    'top_element_style':'large',
                    'elements': [
                        {
                            'title': 'Element',
                            'image_url': 'http://facebook.com/image.jpg',
                            'subtitle': 'Subtitle',
                            'buttons': [
                                {
                                    'type': 'web_url',
                                    'title': 'Web button',
                                    'url': 'http://facebook.com'
                                }
                            ]
                        },
                        {
                            'title': 'Element',
                            'image_url': 'http://facebook.com/image.jpg',
                            'subtitle': 'Subtitle',
                            'buttons': [
                                {
                                    'type': 'web_url',
                                    'title': 'Web button',
                                    'url': 'http://facebook.com'
                                }
                            ]
                        }
                    ],
                    'buttons': [
                        {
                            'type': 'web_url',
                            'title': 'Web button',
                            'url': 'http://facebook.com'
                        }
                    ],
                }
            }
        }
        assert expected == res.to_dict()

    def test_media_template(self):
        btn = elements.Button(
            button_type='web_url',
            title='Web button',
            url='http://facebook.com'
        )
        attachment = attachments.Image(attachment_id='12345')
        res = templates.MediaTemplate(attachment, buttons=[btn])
        expected = {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'media',
                    'elements': [
                        {
                            'media_type': 'image',
                            'attachment_id': '12345',
                            'buttons': [
                                {
                                    'type': 'web_url',
                                    'title': 'Web button',
                                    'url': 'http://facebook.com'
                                }
                            ]
                        }
                    ]
                }
            }
        }
        assert expected == res.to_dict()

    def test_media_template_no_buttons(self):
        attachment = attachments.Image(attachment_id='12345')
        res = templates.MediaTemplate(attachment)
        expected = {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'media',
                    'elements': [
                        {
                            'media_type': 'image',
                            'attachment_id': '12345',
                        }
                    ]
                }
            }
        }
        assert expected == res.to_dict()

    def test_media_template_invalid(self):
        bad_attachment = attachments.File(url='https://some/file.doc')
        with pytest.raises(ValueError):
            templates.MediaTemplate(bad_attachment)
