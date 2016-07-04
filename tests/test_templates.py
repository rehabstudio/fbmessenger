import pytest

from fbmessenger import elements, templates


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

    def test_generic_template(self):
        btn = elements.Button(button_type='web_url', title='Web button', url='http://facebook.com')
        elems = elements.Element(
            title='Element',
            item_url='http://facebook.com',
            image_url='http://facebook.com/image.jpg',
            subtitle='Subtitle',
            buttons=[
                btn
            ]
        )
        res = templates.GenericTemplate(elements=[elems])
        expected = {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
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

    def test_generic_template_with_single_element(self):
        btn = elements.Button(button_type='web_url', title='Web button', url='http://facebook.com')
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
