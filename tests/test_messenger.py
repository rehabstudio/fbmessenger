import pytest
from mock import Mock

from fbmessenger import BaseMessenger, thread_settings


@pytest.fixture
def messenger():
    class Messenger(BaseMessenger):
        def messages(self, payload):
            pass

        def message_deliveries(self, payload):
            pass

        def messaging_postbacks(self, payload):
            pass

        def messaging_optins(self, payload):
            pass

        def message_reads(self, payload):
            pass

        def message_echoes(self, payload):
            pass

    return Messenger(page_access_token=12345678, verify_token=1234)


@pytest.fixture
def entry():
    return {
        'sender': {
            'id': 12345678
        }
    }


@pytest.fixture
def payload():
    return {
        'object': 'page',
        'entry': [
            {
                'id': 1234,
                'time': 1457764198246,
                'messaging': [
                    {
                        'sender': {
                            'id': 1234
                        },
                        'recipient': {
                            'id': 1234
                        },
                        'timestamp': 1457764197627,
                        'message': {
                            'mid': 'mid.1457764197618:41d102a3e1ae206a38',
                            'seq': 73,
                            'text': 'hello, world!'
                        }
                    }
                ]
            }
        ]
    }


@pytest.fixture
def payload_delivered():
    return {
        'object': 'page',
        'entry': [
            {
                'id': 1234,
                'time': 1458668856451,
                'messaging': [
                    {
                        'sender': {
                            'id': 1234
                        },
                        'recipient': {
                            'id': 1234
                        },
                        'delivery': {
                            'mids': [
                                'mid.1458668856218:ed81099e15d3f4f233'
                            ],
                            'watermark': 1458668856253,
                            'seq': 37
                        }
                    }
                ]
            }
        ]
    }


@pytest.fixture
def payload_postback():
    return {
        'object': 'page',
        'entry': [
            {
                'id': 1234,
                'time': 1458668856451,
                'messaging': [
                    {
                        'sender': {
                            'id': 1234
                        },
                        'recipient': {
                            'id': 1234
                        },
                        'timestamp': 1457764197627,
                        'postback': {
                            'payload': 'USER_DEFINED_PAYLOAD'
                        }
                    }
                ]
            }
        ]
    }


@pytest.fixture
def payload_optin():
    return {
        'object': 'page',
        'entry': [
            {
                'id': 1234,
                'time': 1458668856451,
                'messaging': [
                    {
                        'sender': {
                            'id': 1234
                        },
                        'recipient': {
                            'id': 1234
                        },
                        'timestamp': 1457764197627,
                        'optin': {
                            'ref': 'PASS_THROUGH_PARAM'
                        }
                    }
                ]
            }
        ]
    }


def test_verify(messenger):
    res = messenger.verify(verify_token=1234, challenge='challenge')
    assert res == 'challenge'


def test_verify_with_incorrect_token(messenger):
    with pytest.raises(ValueError) as err:
        messenger.verify(verify_token=5678, challenge='challenge')
    assert str(err.value) == 'FB_VERIFY_TOKEN does not match.'


def test_get_user_id(messenger, entry):
    messenger.last_message = entry
    res = messenger.get_user_id()
    assert res == messenger.last_message['sender']['id']


def test_messages(messenger, payload):
    mock_messages = Mock()
    messenger.messages = mock_messages
    messenger.handle(payload)
    mock_messages.assert_called_with(payload['entry'][0]['messaging'][0])


def test_message_deliveries(messenger, payload_delivered):
    mock_message_deliveries = Mock()
    messenger.message_deliveries = mock_message_deliveries
    messenger.handle(payload_delivered)
    mock_message_deliveries.assert_called_with(payload_delivered['entry'][0]['messaging'][0])


def test_messaging_postbacks(messenger, payload_postback):
    mock_messaging_postbacks = Mock()
    messenger.messaging_postbacks = mock_messaging_postbacks
    messenger.handle(payload_postback)
    mock_messaging_postbacks.assert_called_with(payload_postback['entry'][0]['messaging'][0])


def test_messaging_optins(messenger, payload_optin):
    mock_messaging_optins = Mock()
    messenger.messaging_optins = mock_messaging_optins
    messenger.handle(payload_optin)
    mock_messaging_optins.assert_called_with(payload_optin['entry'][0]['messaging'][0])


def test_messages_subscribe(messenger, monkeypatch):
    mock = Mock(return_value='subscribe')
    monkeypatch.setattr(messenger.client, 'subscribe_app_to_page', mock)
    res = messenger.subscribe()
    assert mock.called
    assert res == 'subscribe'


def test_get_user(messenger, payload, monkeypatch):
    mock = Mock()
    mock.return_value = {
        'first_name': 'Testy',
        'last_name': 'McTestface',
        'profile': 'profile'
    }
    monkeypatch.setattr(messenger.client, 'get_user_data', mock)
    messenger.handle(payload)
    user = messenger.get_user()
    assert user == {
        'first_name': 'Testy',
        'last_name': 'McTestface',
        'profile': 'profile'
    }


def test_send(messenger, monkeypatch):
    mock = Mock()
    mock.return_value = {
        'success': True
    }
    monkeypatch.setattr(messenger.client, 'send', mock)
    res = messenger.send({'text': 'message'})
    assert res == mock()


def test_set_thread_setting(messenger, monkeypatch):
    mock = Mock()
    mock.return_value = {
        'success': True
    }
    monkeypatch.setattr(messenger.client, 'set_thread_setting', mock)
    welcome_message = thread_settings.GreetingText(text='Welcome message')
    res = messenger.set_thread_setting(welcome_message.to_dict())
    assert res == mock()
