import pytest

from fbmessenger import thread_settings


class TestThreadSettings:

    def test_greeting_text(self):
        res = thread_settings.GreetingText(text='Hello')
        profile = thread_settings.MessengerProfile(greetings=[res])
        expected = {
            'greeting': [{
                'locale': 'default',
                'text': 'Hello',
            }]
        }
        assert expected == profile.to_dict()

    def test_get_started_button(self):
        res = thread_settings.GetStartedButton(payload='payload')
        profile = thread_settings.MessengerProfile(get_started=res)
        expected = {
            'get_started': {
                'payload': 'payload'
            }
        }
        assert expected == profile.to_dict()

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

    def test_persistent_menu_item_web_url_fallback(self):
        res = thread_settings.PersistentMenuItem(
            item_type='web_url',
            title='Link',
            url='https://facebook.com',
            fallback_url='https://facebook.com/fallback'
        )
        expected = {
            'type': 'web_url',
            'title': 'Link',
            'url': 'https://facebook.com',
            'fallback_url': 'https://facebook.com/fallback',
        }
        assert expected == res.to_dict()

    def test_persistent_menu_messenger_extensions(self):
        res = thread_settings.PersistentMenuItem(
            item_type='web_url',
            title='Link',
            payload='payload',
            url='https://facebook.com',
            messenger_extensions=True
        )
        expected = {
            'type': 'web_url',
            'title': 'Link',
            'url': 'https://facebook.com',
            'messenger_extensions': True
        }
        assert expected == res.to_dict()

    def test_persistent_menu_messenger_extensions_invalid(self):
        with pytest.raises(ValueError) as err:
            thread_settings.PersistentMenuItem(
                item_type='postback',
                title='Link',
                payload='payload',
                messenger_extensions=True
            )
        assert str(err.value) == '`messenger_extensions` is only valid for item type `web_url`'

    def test_webview_share_button_invalid(self):
        with pytest.raises(ValueError) as err:
            thread_settings.PersistentMenuItem(
                item_type='postback',
                title='Link',
                payload='payload',
                webview_share_button=False
            )
        assert str(err.value) == '`webview_share_button` is only valid for item type `web_url`'

    def test_webview_height_ratio_invalid(self):
        with pytest.raises(ValueError) as err:
            thread_settings.PersistentMenuItem(
                item_type='postback',
                title='Link',
                payload='payload',
                webview_height_ratio='anything'
            )
        assert str(err.value) == '`webview_height_ratio` is only valid for item type `web_url`'

    def test_webview_height_ratio_invalid_value(self):
        with pytest.raises(ValueError) as err:
            thread_settings.PersistentMenuItem(
                item_type='web_url',
                title='Link',
                url='https://facebook.com',
                webview_height_ratio='anything'
            )
        assert str(err.value) == 'Invalid webview_height_ratio provided.'

    def test_webview_share_button_true(self):
        res = thread_settings.PersistentMenuItem(
            item_type='web_url',
            title='Link',
            payload='payload',
            url='https://facebook.com',
            webview_share_button=True
        )
        expected = {
            'type': 'web_url',
            'title': 'Link',
            'url': 'https://facebook.com',
        }
        assert expected == res.to_dict()

    def test_webview_share_button_false(self):
        res = thread_settings.PersistentMenuItem(
            item_type='web_url',
            title='Link',
            payload='payload',
            url='https://facebook.com',
            webview_share_button=False
        )
        expected = {
            'type': 'web_url',
            'title': 'Link',
            'url': 'https://facebook.com',
            'webview_share_button': 'hide'
        }
        assert expected == res.to_dict()

    def test_webview_height_ratio(self):
        res = thread_settings.PersistentMenuItem(
            item_type='web_url',
            title='Link',
            payload='payload',
            url='https://facebook.com',
            webview_height_ratio='tall',
        )
        expected = {
            'type': 'web_url',
            'title': 'Link',
            'url': 'https://facebook.com',
            'webview_height_ratio': 'tall'
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

    def test_persistent_menu_nested_item(self):
        item = thread_settings.PersistentMenuItem(
            item_type='postback',
            title='Link',
            payload='payload'
        )
        res = thread_settings.PersistentMenuItem(
            item_type='nested',
            title='Nested',
            nested_items=[item],
        )
        expected = {
            'type': 'nested',
            'title': 'Nested',
            'call_to_actions': [{
                'type': 'postback',
                'title': 'Link',
                'payload': 'payload'
                }]
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

    def test_missing_nested_items(self):
        with pytest.raises(ValueError) as err:
            thread_settings.PersistentMenuItem(
                item_type='nested',
                title='Nested',
            )
        assert str(err.value) == '`nested_items` must be supplied for `nested` type menu items.'

    def test_too_many_nested_items(self):
        item = thread_settings.PersistentMenuItem(
            item_type='web_url',
            title='Link',
            url='https://facebook.com'
        )

        with pytest.raises(ValueError) as err:
            thread_settings.PersistentMenuItem(
                item_type='nested',
                title='Nested',
                nested_items=[item] * 6
            )
        assert str(err.value) == 'Cannot have more than 5 nested_items'

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
        assert str(err.value) == '`payload` must be supplied for `postback` type menu items.'

    def test_persistent_menu(self):
        item = thread_settings.PersistentMenuItem(
            item_type='web_url',
            title='Link',
            url='https://facebook.com'
        )
        res = thread_settings.PersistentMenu(menu_items=[item] * 2)
        profile = thread_settings.MessengerProfile(persistent_menus=[res])
        expected = {
            'persistent_menu': [{
                'locale':'default',
                'call_to_actions':[

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
                ],
            }],
        }
        assert expected == profile.to_dict()

    def test_composer_input_disabled(self):
        item = thread_settings.PersistentMenuItem(
            item_type='web_url',
            title='Link',
            url='https://facebook.com'
        )
        res = thread_settings.PersistentMenu(menu_items=[item], composer_input_disabled=True)
        profile = thread_settings.MessengerProfile(persistent_menus=[res])
        expected = {
            'persistent_menu': [{
                'locale':'default',
                'call_to_actions':[
                    {
                        'type': 'web_url',
                        'title': 'Link',
                        'url': 'https://facebook.com'
                    }
                ],
                'composer_input_disabled': True,
            }],
        }
        assert expected == profile.to_dict()

    def test_composer_input_enabled(self):
        res = thread_settings.PersistentMenu(composer_input_disabled=False)
        profile = thread_settings.MessengerProfile(persistent_menus=[res])
        expected = {
            'persistent_menu': [{
                'locale':'default',
                'composer_input_disabled': False,
            }],
        }
        assert expected == profile.to_dict()

    def test_persistent_menu_too_many_items(self):
        item = thread_settings.PersistentMenuItem(
            item_type='web_url',
            title='Link',
            url='https://facebook.com'
        )
        item_list = [item] * 4
        with pytest.raises(ValueError) as err:
            thread_settings.PersistentMenu(menu_items=item_list)
        assert str(err.value) == 'You cannot have more than 3 menu_items in top level.'

    def test_persistent_menu_no_items(self):
        with pytest.raises(ValueError) as err:
            thread_settings.PersistentMenu()
        assert str(err.value) == 'You must supply at least one menu_item.'

    def test_persistent_menu_no_items_input_disabled(self):
        with pytest.raises(ValueError) as err:
            thread_settings.PersistentMenu(composer_input_disabled=True)
        assert str(err.value) == 'You must supply at least one menu_item.'
