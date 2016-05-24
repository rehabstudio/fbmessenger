from mock import Mock
import pytest

from fbmessenger import MessengerClient, elements, templates


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
            'fields': 'first_name,last_name,profile_pic',
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
    resp = client.send_data(payload, entry)

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


def test_set_welcome_message_text(client, monkeypatch):
    mock_post = Mock()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "result": "Successfully added new_thread's CTAs"
    }
    monkeypatch.setattr('requests.post', mock_post)
    client = MessengerClient(page_access_token=12345678)
    resp = client.set_welcome_message({'text': 'Welcome message'})

    assert resp == {"result": "Successfully added new_thread's CTAs"}
    assert mock_post.call_count == 1
    mock_post.assert_called_with(
        'https://graph.facebook.com/v2.6/me/thread_settings',
        params={'access_token': 12345678},
        json={
            'setting_type': 'call_to_actions',
            'thread_state': 'new_thread',
            'call_to_actions': [{
                'message': {
                    'text': 'Welcome message'
                }
            }]
        }

    )


def test_set_welcome_message_structured(client, monkeypatch):
    mock_post = Mock()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "result": "Successfully added new_thread's CTAs"
    }
    monkeypatch.setattr('requests.post', mock_post)
    client = MessengerClient(page_access_token=12345678)

    btn = elements.Button(title='Web button', url='http://facebook.com')
    msg = templates.ButtonTemplate(
        text='Button template',
        buttons=[btn]
    )
    resp = client.set_welcome_message(msg.to_dict())

    assert resp == {"result": "Successfully added new_thread's CTAs"}
    assert mock_post.call_count == 1
    mock_post.assert_called_with(
        'https://graph.facebook.com/v2.6/me/thread_settings',
        params={'access_token': 12345678},
        json={
            'setting_type': 'call_to_actions',
            'thread_state': 'new_thread',
            'call_to_actions': [{
                'message': {
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
            }]
        }
    )


def test_delete_welcome_message(client, monkeypatch):
    mock_post = Mock()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "result": "Successfully added new_thread's CTAs"
    }
    monkeypatch.setattr('requests.post', mock_post)
    client = MessengerClient(page_access_token=12345678)

    resp = client.set_welcome_message()

    assert resp == {"result": "Successfully added new_thread's CTAs"}
    assert mock_post.call_count == 1
    mock_post.assert_called_with(
        'https://graph.facebook.com/v2.6/me/thread_settings',
        params={'access_token': 12345678},
        json={
            'setting_type': 'call_to_actions',
            'thread_state': 'new_thread',
            'call_to_actions': []
        }
    )
