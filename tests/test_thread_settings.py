import pytest

from fbmessenger import thread_settings


class TestThreadSettings:

    def test_greeting_text(self):
        res = thread_settings.GreetingText(text='Hello')
        expected = {
            'setting_type': 'greeting',
            'greeting': {
                'text': 'Hello'
            }
        }
        assert expected == res.to_dict()

    def test_get_started_button(self):
        res = thread_settings.GetStartedButton(payload='payload')
        expected = {
            'setting_type': 'call_to_actions',
            'thread_state': 'new_thread',
            'call_to_actions': [
                {
                    'payload': 'payload'
                }
            ]
        }
        assert expected == res.to_dict()

    def test_persistent_menu_item_web_url(self):
        res = thread_settings.PersistentMenuItem(
            item_type='web_url',
            title='Link',
            url='https://facebook.com'
        )
        expected = {
            'type': 'web_url',
            'title': 'Link',
            'url': 'https://facebook.com'
        }
        assert expected == res.to_dict()

    def test_persistent_menu_item_postback(self):
        res = thread_settings.PersistentMenuItem(
            item_type='postback',
            title='Link',
            payload='payload'
        )
        expected = {
            'type': 'postback',
            'title': 'Link',
            'payload': 'payload'
        }
        assert expected == res.to_dict()

    def test_invalid_item_type(self):
        with pytest.raises(ValueError) as err:
            thread_settings.PersistentMenuItem(
                item_type='invalid',
                title='Link',
                payload='payload'
            )
        assert str(err.value) == 'Invalid item_type provided.'

    def test_invalid_title(self):
        with pytest.raises(ValueError) as err:
            thread_settings.PersistentMenuItem(
                item_type='postback',
                title='x' * 31,
                payload='payload'
            )
        assert str(err.value) == 'Title cannot be longer 30 characters.'

    def test_invalid_payload(self):
        with pytest.raises(ValueError) as err:
            thread_settings.PersistentMenuItem(
                item_type='postback',
                title='Link',
                payload='x' * 1001
            )
        assert str(err.value) == 'Payload cannot be longer 1000 characters.'

    def test_missing_url_for_web_url(self):
        with pytest.raises(ValueError) as err:
            thread_settings.PersistentMenuItem(
                item_type='web_url',
                title='Link',
            )
        assert str(err.value) == '`url` must be supplied for `web_url` type menu items.'

    def test_missing_payload_for_postback(self):
        with pytest.raises(ValueError) as err:
            thread_settings.PersistentMenuItem(
                item_type='postback',
                title='Link',
            )
        assert str(err.value) == '`postback` must be supplied for `payload` type menu items.'

    def test_persistent_menu(self):
        item = thread_settings.PersistentMenuItem(
            item_type='web_url',
            title='Link',
            url='https://facebook.com'
        )
        res = thread_settings.PersistentMenu(menu_items=[item] * 2)
        expected = {
            'setting_type': 'call_to_actions',
            'thread_state': 'existing_thread',
            'call_to_actions': [
                {
                    'type': 'web_url',
                    'title': 'Link',
                    'url': 'https://facebook.com'
                },
                {
                    'type': 'web_url',
                    'title': 'Link',
                    'url': 'https://facebook.com'
                }
            ]
        }
        assert expected == res.to_dict()

    def test_persistent_menu_too_many_items(self):
        item = thread_settings.PersistentMenuItem(
            item_type='web_url',
            title='Link',
            url='https://facebook.com'
        )
        item_list = [item] * 6
        with pytest.raises(ValueError) as err:
            res = thread_settings.PersistentMenu(menu_items=item_list)
        assert str(err.value) == 'You cannot have more than 5 menu_items.'
