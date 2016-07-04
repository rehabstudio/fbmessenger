import pytest

from fbmessenger import elements


class TestElements:
    def test_text(self):
        res = elements.Text('Test Message')
        expected = {
            'text': 'Test Message'
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

    def test_button_with_title_over_limit(self):
        with pytest.raises(ValueError) as err:
            res = elements.Button(button_type='web_url', title='This button text is over the limit',
                                  url='http://facebook.com')
            res.to_dict()
        assert str(err.value) == 'Title cannot be longer 20 characters.'

    def test_element(self):
        btn = elements.Button(button_type='web_url', title='Web button', url='http://facebook.com')
        res = elements.Element(
            title='Element',
            item_url='http://facebook.com',
            image_url='http://facebook.com/image.jpg',
            subtitle='Subtitle',
            buttons=[
                btn
            ]
        )

        expected = {
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
        assert expected == res.to_dict()

    def test_button_type_validation(self):
        with pytest.raises(ValueError) as err:
            elements.Button(button_type='incorrect', title='Button', url='http://facebook.com')
        assert str(err.value) == 'Invalid button_type provided.'

    def test_element_title_validation(self):
        with pytest.raises(ValueError) as err:
            btn = elements.Button(button_type='web_url', title='Web button', url='http://facebook.com')
            res = elements.Element(
                title='This element title is over the allowed number of characters',
                item_url='http://facebook.com',
                image_url='http://facebook.com/image.jpg',
                subtitle='Subtitle',
                buttons=[
                    btn
                ]
            )
            res.to_dict()
        assert str(err.value) == 'Title cannot be longer 45 characters'

    def test_element_subtitle_validation(self):
        with pytest.raises(ValueError) as err:
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
        assert str(err.value) == 'Subtitle cannot be longer 80 characters'

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
