from mock import Mock
import pytest

from fbmessenger import MessengerClient, elements, templates, thread_settings


@pytest.fixture
def client():
    return MessengerClient(page_access_token=12345678)


@pytest.fixture
def entry():
    return {
        'sender': {
            'id': 12345678
        }
    }


def test_get_user_data(client, monkeypatch):
    mock_get = Mock()
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "first_name": "Test",
        "last_name": "User",
        "profile_pic": "profile"
    }
    monkeypatch.setattr('requests.get', mock_get)
    entry = {
        'sender': {
            'id': 12345678
        }
    }
    client = MessengerClient(page_access_token=12345678)
    resp = client.get_user_data(entry)

    assert resp == {"first_name": "Test", "last_name": "User", "profile_pic": "profile"}
    assert mock_get.call_count == 1
    mock_get.assert_called_with(
        'https://graph.facebook.com/v2.6/12345678',
        params={
            'fields': 'first_name,last_name,profile_pic,locale,timezone,gender',
            'access_token': 12345678
        }
    )


def test_subscribe_app_to_page(client, monkeypatch):
    mock_post = Mock()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "success": True
    }
    monkeypatch.setattr('requests.post', mock_post)
    client = MessengerClient(page_access_token=12345678)
    resp = client.subscribe_app_to_page()

    assert resp == {"success": True}
    assert mock_post.call_count == 1
    mock_post.assert_called_with(
        'https://graph.facebook.com/v2.6/me/subscribed_apps',
        params={'access_token': 12345678}
    )


def test_send_data(client, monkeypatch, entry):
    mock_post = Mock()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "recipient_id": 12345678,
        "message_id": "mid.1456970487936:c34767dfe57ee6e339"
    }
    monkeypatch.setattr('requests.post', mock_post)
    client = MessengerClient(page_access_token=12345678)
    payload = {'text': 'Test message'}
    resp = client.send(payload, entry)

    assert resp == {
        "recipient_id": 12345678,
        "message_id": "mid.1456970487936:c34767dfe57ee6e339"
    }
    assert mock_post.call_count == 1
    mock_post.assert_called_with(
        'https://graph.facebook.com/v2.6/me/messages',
        params={'access_token': 12345678},
        json={
            'recipient': {
                'id': entry['sender']['id']
            },
            'message': payload
        }

    )


def test_set_greeting_text(client, monkeypatch):
    mock_post = Mock()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "result": "Successfully added new_thread's CTAs"
    }
    monkeypatch.setattr('requests.post', mock_post)
    client = MessengerClient(page_access_token=12345678)
    welcome_message = thread_settings.GreetingText(text='Welcome message')
    resp = client.set_thread_setting(welcome_message.to_dict())

    assert resp == {"result": "Successfully added new_thread's CTAs"}
    assert mock_post.call_count == 1
    mock_post.assert_called_with(
        'https://graph.facebook.com/v2.6/me/thread_settings',
        params={'access_token': 12345678},
        json={
            'setting_type': 'greeting',
            'greeting': {
                'text': 'Welcome message'
            }
        }
    )


def test_set_greeting_text_too_long(client, monkeypatch):
    mock_post = Mock()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "result": "Successfully added new_thread's CTAs"
    }
    monkeypatch.setattr('requests.post', mock_post)
    client = MessengerClient(page_access_token=12345678)

    with pytest.raises(ValueError) as err:
        welcome_message = thread_settings.GreetingText(text='x' * 161)
    assert str(err.value) == 'Text cannot be longer 160 characters.'
