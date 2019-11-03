import logging

import pytest

from fbmessenger import elements
from fbmessenger import quick_replies
from fbmessenger.templates import GenericTemplate
from fbmessenger.error_messages import CHARACTER_LIMIT_MESSAGE


class TestElements:
    def test_text(self):
        res = elements.Text('Test Message')
        expected = {
            'text': 'Test Message'
        }
        assert expected == res.to_dict()

    def test_text_with_quick_replies(self):
        qr = quick_replies.QuickReply(title='QR', payload='QR payload')
        qrs = quick_replies.QuickReplies(quick_replies=[qr] * 2)

        res = elements.Text(text='Test Message', quick_replies=qrs)
        expected = {
            'text': 'Test Message',
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
                }
            ]
        }
        assert expected == res.to_dict()

    def test_dynamic_text(self):
        res = elements.DynamicText('Hi, {{first_name}}!', 'Hello friend!')
        expected = {
            'dynamic_text': {
                'text': 'Hi, {{first_name}}!',
                'fallback_text': 'Hello friend!',
            },
        }
        assert expected == res.to_dict()

    def test_dynamic_text_with_quick_replies(self):
        qr = quick_replies.QuickReply(title='QR', payload='QR payload')
        qrs = quick_replies.QuickReplies(quick_replies=[qr])
        res = elements.DynamicText('Hi, {{first_name}}!', 'Hello friend!', quick_replies=qrs)
        expected = {
            'dynamic_text': {
                'text': 'Hi, {{first_name}}!',
                'fallback_text': 'Hello friend!',
            },
            'quick_replies': [
                {
                    'content_type': 'text',
                    'title': 'QR',
                    'payload': 'QR payload'
                },
            ],
        }
        assert expected == res.to_dict()

    def test_web_button(self):
        res = elements.Button(button_type='web_url', title='Web button', url='http://facebook.com')
        expected = {
            'type': 'web_url',
            'title': 'Web button',
            'url': 'http://facebook.com'
        }
        assert expected == res.to_dict()

    def test_postback_button(self):
        res = elements.Button(button_type='postback', title='Postback button', payload='payload')
        expected = {
            'type': 'postback',
            'title': 'Postback button',
            'payload': 'payload'
        }
        assert expected == res.to_dict()

    def test_url_button(self):
        res = elements.Button(
            button_type='web_url',
            title='Web button',
            url='http://facebook.com',
            webview_height_ratio='full',
            messenger_extensions=True,
            fallback_url='https://facebook.com'
        )
        expected = {
            'type': 'web_url',
            'title': 'Web button',
            'url': 'http://facebook.com',
            'webview_height_ratio': 'full',
            'messenger_extensions': 'true',
            'fallback_url': 'https://facebook.com'
        }
        assert expected == res.to_dict()

    def test_button_with_title_over_limit(self, caplog):
        with caplog.at_level(logging.WARNING, logger='fbmessenger.elements'):
            res = elements.Button(button_type='web_url',
                                  title='This button text is over the limit',
                                  url='http://facebook.com')
            res.to_dict()
            assert caplog.record_tuples == [
                ('fbmessenger.elements', logging.WARNING,
                  CHARACTER_LIMIT_MESSAGE.format(field='Title', maxsize=20))]

    def test_element(self):
        btn = elements.Button(button_type='web_url', title='Web button', url='http://facebook.com')
        default = elements.Button(button_type='web_url', url='https://facebook.com')
        res = elements.Element(
            title='Element',
            item_url='http://facebook.com',
            image_url='http://facebook.com/image.jpg',
            subtitle='Subtitle',
            default_action=default,
            buttons=[
                btn
            ]
        )

        expected = {
            'title': 'Element',
            'item_url': 'http://facebook.com',
            'image_url': 'http://facebook.com/image.jpg',
            'subtitle': 'Subtitle',
            'default_action': {
                'type': 'web_url',
                'url': 'https://facebook.com'
            },
            'buttons': [
                {
                    'type': 'web_url',
                    'title': 'Web button',
                    'url': 'http://facebook.com'
                }
            ]
        }
        assert expected == res.to_dict()

    def test_default_action_validation(self):
        defaults = [
            (
                elements.Button(button_type='web_url', url='https://facebook.com', title='Facebook'),
                'The default_action button may not have a title'
            ),
            (
                elements.Button(button_type='postback', payload='foo'),
                'The default_action button must be of type web_url'
            )

        ]
        btn = elements.Button(button_type='web_url', title='Web button', url='http://facebook.com')
        for default, msg in defaults:
            with pytest.raises(ValueError) as err:
                elements.Element(
                    title='Element',
                    item_url='http://facebook.com',
                    image_url='http://facebook.com/image.jpg',
                    subtitle='Subtitle',
                    default_action=default,
                    buttons=[
                        btn
                    ]
                )
            assert str(err.value) == msg

    def test_button_type_validation(self):
        with pytest.raises(ValueError) as err:
            elements.Button(button_type='incorrect', title='Button', url='http://facebook.com')
        assert str(err.value) == 'Invalid button_type provided.'

    def test_button_webview_height_ratio_validation(self):
        with pytest.raises(ValueError) as err:
            elements.Button(
                button_type='web_url',
                title='Button',
                url='http://facebook.com',
                webview_height_ratio='wrong'
            )
        assert str(err.value) == 'Invalid webview_height_ratio provided.'

    def test_element_title_validation(self, caplog):
        with caplog.at_level(logging.WARNING, logger='fbmessenger.elements'):
            btn = elements.Button(button_type='web_url', title='Web button', url='http://facebook.com')
            res = elements.Element(
                title='The title is too long and should throw an error.'
                       'The maximum allowed number of characters is 80',
                item_url='http://facebook.com',
                image_url='http://facebook.com/image.jpg',
                subtitle='Subtitle',
                buttons=[
                    btn
                ]
            )
            res.to_dict()
            assert caplog.record_tuples == [
                ('fbmessenger.elements', logging.WARNING,
                  CHARACTER_LIMIT_MESSAGE.format(field='Title', maxsize=80))]

    def test_element_subtitle_validation(self, caplog):
        with caplog.at_level(logging.WARNING, logger='fbmessenger.elements'):
            btn = elements.Button(button_type='web_url', title='Web button', url='http://facebook.com')
            res = elements.Element(
                title='Title',
                item_url='http://facebook.com',
                image_url='http://facebook.com/image.jpg',
                subtitle='The subtitle is too long and should throw an error.'
                         'The maximum allowed number of characters is 80',
                buttons=[
                    btn
                ]
            )
            res.to_dict()
            assert caplog.record_tuples == [
                ('fbmessenger.elements', logging.WARNING,
                  CHARACTER_LIMIT_MESSAGE.format(field='Subtitle', maxsize=80))]

    def test_adjustment(self):
        res = elements.Adjustment(name='discount', amount=1)
        expected = {
            'name': 'discount',
            'amount': 1
        }
        assert expected == res.to_dict()

    def test_address(self):
        res = elements.Address(street_1='street_1', street_2='street_2', city='city',
                               postal_code='postal_code', state='state', country='country')
        expected = {
            'street_1': 'street_1',
            'street_2': 'street_2',
            'city': 'city',
            'postal_code': 'postal_code',
            'state': 'state',
            'country': 'country',
        }
        assert expected == res.to_dict()

    def test_summary(self):
        res = elements.Summary(subtotal='10', shipping_cost='5', total_tax='17.5', total_cost='100')
        expected = {
            'subtotal': '10',
            'shipping_cost': '5',
            'total_tax': '17.5',
            'total_cost': '100'
        }
        assert expected == res.to_dict()
