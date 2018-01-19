from mock import Mock
import pytest

from fbmessenger import (
    MessengerClient,
    attachments,
    quick_replies,
    thread_settings,
)


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
    monkeypatch.setattr('requests.Session.get', mock_get)
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
        'https://graph.facebook.com/v2.11/12345678',
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
    monkeypatch.setattr('requests.Session.post', mock_post)
    client = MessengerClient(page_access_token=12345678)
    resp = client.subscribe_app_to_page()

    assert resp == {"success": True}
    assert mock_post.call_count == 1
    mock_post.assert_called_with(
        'https://graph.facebook.com/v2.11/me/subscribed_apps',
        params={'access_token': 12345678}
    )


def test_send_data(client, monkeypatch, entry):
    mock_post = Mock()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "recipient_id": 12345678,
        "message_id": "mid.1456970487936:c34767dfe57ee6e339"
    }
    monkeypatch.setattr('requests.Session.post', mock_post)
    client = MessengerClient(page_access_token=12345678)
    payload = {'text': 'Test message'}
    resp = client.send(payload, entry, 'RESPONSE')

    assert resp == {
        "recipient_id": 12345678,
        "message_id": "mid.1456970487936:c34767dfe57ee6e339"
    }
    assert mock_post.call_count == 1
    mock_post.assert_called_with(
        'https://graph.facebook.com/v2.11/me/messages',
        params={'access_token': 12345678},
        json={
            'messaging_type': 'RESPONSE',
            'recipient': {
                'id': entry['sender']['id']
            },
            'message': payload
        }
    )


def test_send_data_invalid_message_type():
    client = MessengerClient(page_access_token=12345678)
    payload = {'text': 'Test message'}
    with pytest.raises(ValueError):
        client.send(payload, entry, 'INVALID')


def test_send_action(client, monkeypatch, entry):
    mock_post = Mock()
    mock_post.return_value.status_code = 200
    monkeypatch.setattr('requests.Session.post', mock_post)
    client = MessengerClient(page_access_token=12345678)
    client.send_action('typing_on', entry)

    assert mock_post.call_count == 1
    mock_post.assert_called_with(
        'https://graph.facebook.com/v2.11/me/messages',
        params={'access_token': 12345678},
        json={
            'recipient': {
                'id': entry['sender']['id']
            },
            'sender_action': 'typing_on'
        }
    )


def test_set_greeting_text(client, monkeypatch):
    mock_post = Mock()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "result": "success"
    }
    monkeypatch.setattr('requests.Session.post', mock_post)
    client = MessengerClient(page_access_token=12345678)
    welcome_message = thread_settings.GreetingText(text='Welcome message')
    profile = thread_settings.MessengerProfile(greetings=[welcome_message])
    resp = client.set_messenger_profile(profile.to_dict())

    assert resp == {"result": "success"}
    assert mock_post.call_count == 1
    mock_post.assert_called_with(
        'https://graph.facebook.com/v2.11/me/messenger_profile',
        params={'access_token': 12345678},
        json={
            'greeting': [{
                'locale': 'default',
                'text': 'Welcome message'
            }]
        }
    )


def test_set_greeting_text_too_long(client, monkeypatch):
    mock_post = Mock()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "result": "success"
    }
    monkeypatch.setattr('requests.Session.post', mock_post)

    with pytest.raises(ValueError) as err:
        thread_settings.GreetingText(text='x' * 161)
    assert str(err.value) == 'Text cannot be longer 160 characters.'


def test_delete_get_started(client, monkeypatch):
    mock_delete = Mock()
    mock_delete.return_value.status_code = 200
    monkeypatch.setattr('requests.Session.delete', mock_delete)
    client = MessengerClient(page_access_token=12345678)
    client.delete_get_started()

    assert mock_delete.call_count == 1
    mock_delete.assert_called_with(
        'https://graph.facebook.com/v2.11/me/messenger_profile',
        params={'access_token': 12345678},
        json={
            'fields': [
                'get_started',
            ],
        }
    )


def test_delete_persistent_menu(client, monkeypatch):
    mock_delete = Mock()
    mock_delete.return_value.status_code = 200
    monkeypatch.setattr('requests.Session.delete', mock_delete)
    client = MessengerClient(page_access_token=12345678)
    client.delete_persistent_menu()

    assert mock_delete.call_count == 1
    mock_delete.assert_called_with(
        'https://graph.facebook.com/v2.11/me/messenger_profile',
        params={'access_token': 12345678},
        json={
            'fields': [
                'persistent_menu',
            ],
        }
    )


def test_link_account(client, monkeypatch):
    mock_post = Mock()
    mock_post.return_value.status_code = 200
    monkeypatch.setattr('requests.Session.post', mock_post)
    client = MessengerClient(page_access_token=12345678)
    client.link_account(1234)

    assert mock_post.call_count == 1
    mock_post.assert_called_with(
        'https://graph.facebook.com/v2.11/me',
        params={
            'access_token': 12345678,
            'fields': 'recipient',
            'account_linking_token': 1234
        }
    )


def test_unlink_account(client, monkeypatch):
    mock_post = Mock()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "result": "unlink account success"
    }
    monkeypatch.setattr('requests.Session.post', mock_post)
    client = MessengerClient(page_access_token=12345678)
    res = client.unlink_account(1234)
    assert res == {"result": "unlink account success"}
    assert mock_post.call_count == 1
    mock_post.assert_called_with(
        'https://graph.facebook.com/v2.11/me/unlink_accounts',
        params={
            'access_token': 12345678,
        },
        json={
            'psid': 1234
        }
    )


def test_add_whitelisted_domains(client, monkeypatch):
    mock_post = Mock()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "result": "success",
    }
    monkeypatch.setattr('requests.Session.post', mock_post)
    client = MessengerClient(page_access_token=12345678)
    res = client.update_whitelisted_domains(['https://facebook.com'])
    assert res == {"result": "success"}
    assert mock_post.call_count == 1
    mock_post.assert_called_with(
        'https://graph.facebook.com/v2.11/me/messenger_profile',
        params={
            'access_token': 12345678,
        },
        json={
            'whitelisted_domains': [
                'https://facebook.com'
            ],
        }
    )


def test_add_whitelisted_domains_not_as_list(client, monkeypatch):
    mock_post = Mock()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "result": "success",
    }
    monkeypatch.setattr('requests.Session.post', mock_post)
    client = MessengerClient(page_access_token=12345678)
    res = client.update_whitelisted_domains('https://facebook.com')
    assert res == {"result": "success"}
    assert mock_post.call_count == 1
    mock_post.assert_called_with(
        'https://graph.facebook.com/v2.11/me/messenger_profile',
        params={
            'access_token': 12345678,
        },
        json={
            'whitelisted_domains': [
                'https://facebook.com'
            ],
        }
    )


def test_remove_whitelisted_domains(client, monkeypatch):
    mock_post = Mock()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "result": "success",
    }
    monkeypatch.setattr('requests.Session.delete', mock_post)
    client = MessengerClient(page_access_token=12345678)
    res = client.remove_whitelisted_domains()
    assert res == {"result": "success"}
    assert mock_post.call_count == 1
    mock_post.assert_called_with(
        'https://graph.facebook.com/v2.11/me/messenger_profile',
        params={
            'access_token': 12345678,
        },
        json={
            'fields': [
                'whitelisted_domains',
            ],
        }
    )


def test_upload_attachment(monkeypatch):
    mock_post = Mock()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "attachment_id": "12345",
    }
    monkeypatch.setattr('requests.Session.post', mock_post)

    attachment = attachments.Image(url='https://some-image.com/image.jpg')
    client = MessengerClient(page_access_token=12345678)
    res = client.upload_attachment(attachment)
    assert res == {"attachment_id": "12345"}
    assert mock_post.call_count == 1
    mock_post.assert_called_with(
        'https://graph.facebook.com/v2.11/me/message_attachments',
        params={
            'access_token': 12345678,
        },
        json={
            'message': {
                'attachment': {
                    'type': 'image',
                    'payload': {
                        'url': 'https://some-image.com/image.jpg'
                    }
                }
            }
        }
    )


def test_upload_url_required():
    attachment = attachments.Image(attachment_id='12345')
    client = MessengerClient(page_access_token=12345678)
    with pytest.raises(ValueError):
        client.upload_attachment(attachment)


def test_upload_no_quick_replies():
    replies = quick_replies.QuickReplies(
        [quick_replies.QuickReply(title='hello', payload='hello')])
    attachment = attachments.Image(
        url='https://some-image.com/image.jpg', quick_replies=replies)
    client = MessengerClient(page_access_token=12345678)
    with pytest.raises(ValueError):
        client.upload_attachment(attachment)
