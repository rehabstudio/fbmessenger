import copy
import pytest
from mock import Mock

from fbmessenger import BaseMessenger, thread_settings


@pytest.fixture
def messenger():
    class Messenger(BaseMessenger):
        def message(self, payload):
            pass

        def delivery(self, payload):
            pass

        def postback(self, payload):
            pass

        def optin(self, payload):
            pass

        def read(self, payload):
            pass

        def account_linking(self, payload):
            pass

    return Messenger(page_access_token=12345678)


base_payload = {
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
                }
            ]
        }
    ]
}


@pytest.fixture
def entry():
    return {
        'sender': {
            'id': 12345678
        }
    }


@pytest.fixture
def recipient_id():
    return 12345678


@pytest.fixture
def payload_message():
    payload1 = copy.deepcopy(base_payload)
    payload1['entry'][0]['messaging'][0]['message'] = {
        'mid': 'mid.1457764197618:41d102a3e1ae206a38',
        'seq': 73,
        'text': 'hello, world!'
    }
    return payload1


@pytest.fixture
def payload_message_read():
    payload2 = copy.deepcopy(base_payload)
    payload2['entry'][0]['messaging'][0]['read'] = {
        'watermark': 1458668856253,
        'seq': 38
    }
    return payload2


@pytest.fixture
def payload_account_linking():
    payload = copy.deepcopy(base_payload)
    payload['entry'][0]['messaging'][0]['account_linking'] = {
        'status': 'linked',
        'authorization_code': 'PASS_THROUGH_AUTHORIZATION_CODE'
    }
    return payload


@pytest.fixture
def payload_delivered():
    payload = copy.deepcopy(base_payload)
    payload['entry'][0]['messaging'][0]['delivery'] = {
        'mids': [
            'mid.1458668856218:ed81099e15d3f4f233'
        ],
        'watermark': 1458668856253,
        'seq': 37
    }
    return payload


@pytest.fixture
def payload_postback():
    payload = copy.deepcopy(base_payload)
    payload['entry'][0]['messaging'][0]['postback'] = {
        'payload': 'USER_DEFINED_PAYLOAD'
    }
    return payload


@pytest.fixture
def payload_optin():
    payload = copy.deepcopy(base_payload)
    payload['entry'][0]['messaging'][0]['optin'] = {
        'ref': 'PASS_THROUGH_PARAM'
    }
    return payload


def test_get_user_id(messenger, entry):
    messenger.last_message = entry
    res = messenger.get_user_id()
    assert res == messenger.last_message['sender']['id']


def test_get_user_id_not_exists(messenger):
    messenger.last_message = {}
    with pytest.raises(KeyError):
        messenger.get_user_id()


def test_messages(messenger, payload_message):
    mock_message = Mock()
    messenger.message = mock_message
    messenger.handle(payload_message)
    mock_message.assert_called_with(payload_message['entry'][0]['messaging'][0])


def test_message_deliveries(messenger, payload_delivered):
    mock_delivery = Mock()
    messenger.delivery = mock_delivery
    messenger.handle(payload_delivered)
    mock_delivery.assert_called_with(payload_delivered['entry'][0]['messaging'][0])


def test_messaging_postbacks(messenger, payload_postback):
    mock_postback = Mock()
    messenger.postback = mock_postback
    messenger.handle(payload_postback)
    mock_postback.assert_called_with(payload_postback['entry'][0]['messaging'][0])


def test_messaging_optins(messenger, payload_optin):
    mock_optin = Mock()
    messenger.optin = mock_optin
    messenger.handle(payload_optin)
    mock_optin.assert_called_with(payload_optin['entry'][0]['messaging'][0])


def test_message_reads(messenger, payload_message_read):
    mock_read = Mock()
    messenger.read = mock_read
    messenger.handle(payload_message_read)
    mock_read.assert_called_with(payload_message_read['entry'][0]['messaging'][0])


def test_subscribe(messenger, monkeypatch):
    mock = Mock(return_value='subscribe')
    monkeypatch.setattr(messenger.client, 'subscribe_app_to_page', mock)
    res = messenger.subscribe_app_to_page()
    assert mock.called
    assert res == 'subscribe'


def test_account_linking(messenger, payload_account_linking):
    mock_account_linking = Mock()
    messenger.account_linking = mock_account_linking
    messenger.handle(payload_account_linking)
    mock_account_linking.assert_called_with(payload_account_linking['entry'][0]['messaging'][0])


def test_get_user(messenger, monkeypatch, recipient_id):
    mock = Mock()
    mock.return_value = {
        'first_name': 'Testy',
        'last_name': 'McTestface',
        'profile': 'profile'
    }
    monkeypatch.setattr(messenger.client, 'get_user_data', mock)
    monkeypatch.setattr(messenger, 'get_user_id', lambda: recipient_id)
    user = messenger.get_user()
    assert user == {
        'first_name': 'Testy',
        'last_name': 'McTestface',
        'profile': 'profile'
    }
    mock.assert_called_with(recipient_id, fields=None, timeout=None)


def test_send(messenger, monkeypatch, recipient_id):
    mock = Mock()
    mock.return_value = {
        'success': True
    }
    monkeypatch.setattr(messenger.client, 'send', mock)
    monkeypatch.setattr(messenger, 'get_user_id', lambda: recipient_id)
    res = messenger.send({'text': 'message'}, 'RESPONSE')
    assert res == mock.return_value
    mock.assert_called_with({'text': 'message'}, recipient_id, messaging_type='RESPONSE', notification_type='REGULAR',
                            timeout=None, tag=None)


def test_send_action(messenger, monkeypatch, recipient_id):
    mock = Mock()
    monkeypatch.setattr(messenger.client, 'send_action', mock)
    monkeypatch.setattr(messenger, 'get_user_id', lambda: recipient_id)
    res = messenger.send_action('typing_on')
    assert res == mock.return_value
    mock.assert_called_with('typing_on', recipient_id, timeout=None)


def test_set_thread_setting(messenger, monkeypatch):
    mock = Mock()
    mock.return_value = {
        'success': True
    }
    monkeypatch.setattr(messenger.client, 'set_messenger_profile', mock)
    welcome_message = thread_settings.GreetingText(text='Welcome message')
    profile = thread_settings.MessengerProfile(greetings=[welcome_message])
    res = messenger.set_messenger_profile(profile.to_dict())
    assert res == mock.return_value
    greeting = {
        'greeting': [{
            'locale': 'default',
            'text': 'Welcome message'
        }]
    }
    mock.assert_called_with(greeting, timeout=None)


def test_delete_get_started(messenger, monkeypatch):
    mock = Mock()
    mock.return_value = {
        'success': True
    }
    monkeypatch.setattr(messenger.client, 'delete_get_started', mock)
    res = messenger.delete_get_started()
    assert res == mock.return_value
    mock.assert_called_with(timeout=None)


def test_link_account(messenger, monkeypatch):
    mock = Mock()
    monkeypatch.setattr(messenger.client, 'link_account', mock)
    res = messenger.link_account(1234)
    assert res == mock.return_value
    mock.assert_called_with(1234, timeout=None)


def test_unlink_account(messenger, monkeypatch):
    mock = Mock()
    mock.return_value = {
        'success': True
    }
    monkeypatch.setattr(messenger.client, 'unlink_account', mock)
    res = messenger.unlink_account(1234)
    assert res == mock.return_value
    mock.assert_called_with(1234, timeout=None)


def test_add_whitelisted_domains(messenger, monkeypatch):
    mock = Mock()
    mock.return_value = {
        'success': True
    }
    monkeypatch.setattr(messenger.client, 'update_whitelisted_domains', mock)
    res = messenger.add_whitelisted_domains('https://facebook.com')
    assert res == mock.return_value
    mock.assert_called_with('https://facebook.com', timeout=None)


def test_remove_whitelisted_domains(messenger, monkeypatch):
    mock = Mock()
    mock.return_value = {
        'success': True
    }
    monkeypatch.setattr(messenger.client, 'remove_whitelisted_domains', mock)
    res = messenger.remove_whitelisted_domains()
    assert res == mock.return_value
    mock.assert_called_with(timeout=None)


def test_upload_attachment(messenger, monkeypatch):
    mock = Mock()
    mock.return_value = {
        'attachment_id': 12345
    }
    monkeypatch.setattr(messenger.client, 'upload_attachment', mock)
    attachment = {'some': 'data'}
    res = messenger.upload_attachment(attachment)
    assert res == mock.return_value
    mock.assert_called_with(attachment, timeout=None)
