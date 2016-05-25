import pytest
from mock import Mock

from fbmessenger import BaseMessenger


@pytest.fixture
def client():
    return BaseMessenger(page_access_token=12345678, verify_token=1234)


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
    assert str(err.value) == 'FB_VERIFY_TOKEN does not match.'


def test_get_user_id(client, entry):
    client.last_message = entry
    res = client.get_user_id()
    assert res == client.last_message['sender']['id']


def test_messages_throws_exception(client):
    with pytest.raises(NotImplementedError) as err:
        client.messages('')
    assert str(err.value) == '`messages` is not implemented.'


def test_message_deliveries_throws_exception(client):
    with pytest.raises(NotImplementedError) as err:
        client.message_deliveries('')
    assert str(err.value) == '`message_deliveries` is not implemented.'


def test_messaging_postbacks_throws_exception(client):
    with pytest.raises(NotImplementedError) as err:
        client.messaging_postbacks('')
    assert str(err.value) == '`messaging_postbacks` is not implemented.'


def test_messaging_optins_throws_exception(client):
    with pytest.raises(NotImplementedError) as err:
        client.messaging_optins('')
    assert str(err.value) == '`messaging_optins` is not implemented.'


def test_messages(client, payload, monkeypatch):
    mock_messages = Mock()
    client.messages = mock_messages
    client.handle(payload)
    mock_messages.assert_called_with(payload['entry'][0]['messaging'][0])


def test_message_deliveries(client, payload_delivered, monkeypatch):
    mock_message_deliveries = Mock()
    client.message_deliveries = mock_message_deliveries
    client.handle(payload_delivered)
    mock_message_deliveries.assert_called_with(payload_delivered['entry'][0]['messaging'][0])
