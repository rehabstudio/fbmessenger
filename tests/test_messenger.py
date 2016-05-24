import pytest
from mock import Mock

from fbmessenger import Messenger


@pytest.fixture
def client():
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


def test_verify(client):
    res = client.verify(verify_token=1234, challenge='challenge')
    assert res == 'challenge'


def test_verify_with_incorrect_token(client):
    with pytest.raises(ValueError) as err:
        client.verify(verify_token=5678, challenge='challenge')
    assert err.value.message == 'FB_VERIFY_TOKEN does not match.'


def test_get_user_id(client, entry):
    client.last_message = entry
    res = client.get_user_id()
    assert res == client.last_message['sender']['id']


def test_handle_message_received_throws_exception(client):
    with pytest.raises(NotImplementedError) as err:
        client.handle_message_received('')
    assert err.value.message == 'Please implement `handle_message_received` to process messages.'


def test_handle_message_delivered_throws_exception(client):
    with pytest.raises(NotImplementedError) as err:
        client.handle_message_delivered('')
    assert err.value.message == 'Please implement `handle_message_delivered` to process delivery messages.'


def test_handle_postback_throws_exception(client):
    with pytest.raises(NotImplementedError) as err:
        client.handle_postback('')
    assert err.value.message == 'Please implement `handle_postback` to process postbacks.'


def test_handle_optin_throws_exception(client):
    with pytest.raises(NotImplementedError) as err:
        client.handle_optin('')
    assert err.value.message == 'Please implement `handle_optin` to process optins.'


def test_handle_message_received(client, payload, monkeypatch):
    mock_handle_message = Mock()
    client.handle_message_received = mock_handle_message
    client.handle(payload)
    mock_handle_message.assert_called_with(payload['entry'][0]['messaging'][0])


def test_handle_message_delivered(client, payload_delivered, monkeypatch):
    mock_handle_message = Mock()
    client.handle_message_delivered = mock_handle_message
    client.handle(payload_delivered)
    mock_handle_message.assert_called_with(payload_delivered['entry'][0]['messaging'][0])
