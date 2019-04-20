import requests
import mock
import pytest

from fbmessenger import (
    MessengerClient,
    attachments,
    quick_replies,
    thread_settings,
)


@pytest.fixture
def client():
    return MessengerClient(page_access_token=12345678, api_version=2.12, app_secret=12345678)


@pytest.fixture
def recipient_id():
    return 987654321


@pytest.fixture
def default_params():
    return {
        'access_token': 12345678,
        'appsecret_proof': 'e220691b3e23647fc17c4b282bb469ac77fbadb8f5c77898294e42de95add560',
    }


def test_get_user_data(client, monkeypatch, recipient_id, default_params):
    mock_get = mock.Mock()
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "first_name": "Test",
        "last_name": "User",
        "profile_pic": "profile"
    }
    monkeypatch.setattr('requests.Session.get', mock_get)
    resp = client.get_user_data(recipient_id)

    assert resp == {"first_name": "Test", "last_name": "User", "profile_pic": "profile"}
    assert mock_get.call_count == 1
    mock_get.assert_called_with(
        'https://graph.facebook.com/v{api_version}/{recipient_id}'.format(api_version=client.api_version,
                                                                          recipient_id=recipient_id),
        params=dict({
            'fields': 'first_name,last_name,profile_pic,locale,timezone,gender',
        }, **default_params),
        timeout=None
    )


def test_get_user_data_fields_string(client, monkeypatch, recipient_id, default_params):
    mock_get = mock.Mock()
    mock_get.return_value.status_code == 200
    mock_get.return_value.json.return_value = {
        "first_name": "Test",
        "last_name": "User",
    }
    monkeypatch.setattr('requests.Session.get', mock_get)
    resp = client.get_user_data(recipient_id, fields='first_name,last_name')

    assert resp == {"first_name": "Test", "last_name": "User"}
    assert mock_get.call_count == 1
    mock_get.assert_called_with(
        'https://graph.facebook.com/v{api_version}/{recipient_id}'.format(api_version=client.api_version,
                                                                          recipient_id=recipient_id),
        params=dict({
            'fields': 'first_name,last_name',
        }, **default_params),
        timeout=None
    )


def test_get_user_data_fields_list(client, monkeypatch, recipient_id, default_params):
    mock_get = mock.Mock()
    mock_get.return_value.status_code == 200
    mock_get.return_value.json.return_value = {
        "first_name": "Test",
        "last_name": "User",
    }
    monkeypatch.setattr('requests.Session.get', mock_get)
    resp = client.get_user_data(recipient_id, fields=['first_name', 'last_name'])

    assert resp == {"first_name": "Test", "last_name": "User"}
    assert mock_get.call_count == 1
    mock_get.assert_called_with(
        'https://graph.facebook.com/v{api_version}/{recipient_id}'.format(api_version=client.api_version,
                                                                          recipient_id=recipient_id),
        params=dict({
            'fields': 'first_name,last_name',
        }, **default_params),
        timeout=None
    )


def test_get_user_data_fields_tuple(client, monkeypatch, recipient_id, default_params):
    mock_get = mock.Mock()
    mock_get.return_value.status_code == 200
    mock_get.return_value.json.return_value = {
        "first_name": "Test",
        "last_name": "User",
    }
    monkeypatch.setattr('requests.Session.get', mock_get)
    resp = client.get_user_data(recipient_id, fields=('first_name', 'last_name'))

    assert resp == {"first_name": "Test", "last_name": "User"}
    assert mock_get.call_count == 1
    mock_get.assert_called_with(
        'https://graph.facebook.com/v{api_version}/{recipient_id}'.format(api_version=client.api_version,
                                                                          recipient_id=recipient_id),
        params=dict({
            'fields': 'first_name,last_name',
        }, **default_params),
        timeout=None
    )


def test_subscribe_app_to_page(client, monkeypatch, default_params):
    mock_post = mock.Mock()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "success": True
    }
    monkeypatch.setattr('requests.Session.post', mock_post)
    resp = client.subscribe_app_to_page()

    assert resp == {"success": True}
    assert mock_post.call_count == 1
    mock_post.assert_called_with(
        'https://graph.facebook.com/v{api_version}/me/subscribed_apps'.format(api_version=client.api_version),
        params=default_params,
        timeout=None
    )


def test_send_data(client, monkeypatch, recipient_id, default_params):
    mock_post = mock.Mock()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "recipient_id": recipient_id,
        "message_id": "mid.1456970487936:c34767dfe57ee6e339"
    }
    monkeypatch.setattr('requests.Session.post', mock_post)
    payload = {'text': 'Test message'}
    resp = client.send(payload, recipient_id, 'RESPONSE')

    assert resp == {
        "recipient_id": recipient_id,
        "message_id": "mid.1456970487936:c34767dfe57ee6e339",
    }
    assert mock_post.call_count == 1
    mock_post.assert_called_with(
        'https://graph.facebook.com/v{api_version}/me/messages'.format(api_version=client.api_version),
        params=default_params,
        json={
            'messaging_type': 'RESPONSE',
            'notification_type': 'REGULAR',
            'recipient': {
                'id': recipient_id,
            },
            'message': payload,
        },
        timeout=None
    )


def test_send_data_notification_type(client, monkeypatch, recipient_id, default_params):
    mock_post = mock.Mock()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "recipient_id": recipient_id,
        "message_id": "mid.1456970487936:c34767dfe57ee6e339"
    }
    monkeypatch.setattr('requests.Session.post', mock_post)
    payload = {'text': 'Test message'}
    client.send(payload, recipient_id, 'RESPONSE', notification_type='SILENT_PUSH')

    mock_post.assert_called_with(
        'https://graph.facebook.com/v{api_version}/me/messages'.format(api_version=client.api_version),
        params=default_params,
        json={
            'messaging_type': 'RESPONSE',
            'notification_type': 'SILENT_PUSH',
            'recipient': {
                'id': recipient_id,
            },
            'message': payload,
        },
        timeout=None
    )


def test_send_data_invalid_notification_type(client, recipient_id):
    payload = {'text': 'Test message'}
    with pytest.raises(ValueError):
        client.send(payload, recipient_id, 'RESPONSE', notification_type='INVALID')


def test_send_data_invalid_message_type(client, recipient_id):
    payload = {'text': 'Test message'}
    with pytest.raises(ValueError):
        client.send(payload, recipient_id, 'INVALID')


def test_send_data_with_tag(client, monkeypatch, recipient_id, default_params):
    mock_post = mock.Mock()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "recipient_id": recipient_id,
        "message_id": "mid.1456970487936:c34767dfe57ee6e339"
    }
    monkeypatch.setattr('requests.Session.post', mock_post)
    payload = {'text': 'Test message'}
    client.send(payload, recipient_id, 'MESSAGE_TAG', tag='ACCOUNT_UPDATE')

    mock_post.assert_called_with(
        'https://graph.facebook.com/v{api_version}/me/messages'.format(api_version=client.api_version),
        params=default_params,
        json={
            'messaging_type': 'MESSAGE_TAG',
            'notification_type': 'REGULAR',
            'recipient': {
                'id': recipient_id,
            },
            'message': payload,
            'tag': 'ACCOUNT_UPDATE',
        },
        timeout=None
    )


def test_send_action(client, monkeypatch, recipient_id, default_params):
    mock_post = mock.Mock()
    mock_post.return_value.status_code = 200
    monkeypatch.setattr('requests.Session.post', mock_post)
    client.send_action('typing_on', recipient_id)

    assert mock_post.call_count == 1
    mock_post.assert_called_with(
        'https://graph.facebook.com/v{api_version}/me/messages'.format(api_version=client.api_version),
        params=default_params,
        json={
            'recipient': {
                'id': recipient_id,
            },
            'sender_action': 'typing_on',
        },
        timeout=None
    )


def test_set_greeting_text(client, monkeypatch, default_params):
    mock_post = mock.Mock()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "result": "success"
    }
    monkeypatch.setattr('requests.Session.post', mock_post)
    welcome_message = thread_settings.GreetingText(text='Welcome message')
    profile = thread_settings.MessengerProfile(greetings=[welcome_message])
    resp = client.set_messenger_profile(profile.to_dict())

    assert resp == {"result": "success"}
    assert mock_post.call_count == 1
    mock_post.assert_called_with(
        'https://graph.facebook.com/v{api_version}/me/messenger_profile'.format(api_version=client.api_version),
        params=default_params,
        json={
            'greeting': [{
                'locale': 'default',
                'text': 'Welcome message',
            }]
        },
        timeout=None
    )


def test_set_greeting_text_too_long(monkeypatch):
    mock_post = mock.Mock()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "result": "success"
    }
    monkeypatch.setattr('requests.Session.post', mock_post)

    with pytest.raises(ValueError) as err:
        thread_settings.GreetingText(text='x' * 161)
    assert str(err.value) == 'Text cannot be longer 160 characters.'


def test_delete_get_started(client, monkeypatch, default_params):
    mock_delete = mock.Mock()
    mock_delete.return_value.status_code = 200
    monkeypatch.setattr('requests.Session.delete', mock_delete)
    client.delete_get_started()

    assert mock_delete.call_count == 1
    mock_delete.assert_called_with(
        'https://graph.facebook.com/v{api_version}/me/messenger_profile'.format(api_version=client.api_version),
        params=default_params,
        json={
            'fields': [
                'get_started',
            ],
        },
        timeout=None
    )


def test_delete_persistent_menu(client, monkeypatch, default_params):
    mock_delete = mock.Mock()
    mock_delete.return_value.status_code = 200
    monkeypatch.setattr('requests.Session.delete', mock_delete)
    client.delete_persistent_menu()

    assert mock_delete.call_count == 1
    mock_delete.assert_called_with(
        'https://graph.facebook.com/v{api_version}/me/messenger_profile'.format(api_version=client.api_version),
        params=default_params,
        json={
            'fields': [
                'persistent_menu',
            ],
        },
        timeout=None
    )


def test_link_account(client, monkeypatch, default_params):
    mock_post = mock.Mock()
    mock_post.return_value.status_code = 200
    monkeypatch.setattr('requests.Session.post', mock_post)
    client.link_account(1234)

    assert mock_post.call_count == 1
    mock_post.assert_called_with(
        'https://graph.facebook.com/v{api_version}/me'.format(api_version=client.api_version),
        params=dict({
            'fields': 'recipient',
            'account_linking_token': 1234,
        }, **default_params),
        timeout=None
    )


def test_unlink_account(client, monkeypatch, default_params):
    mock_post = mock.Mock()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "result": "unlink account success"
    }
    monkeypatch.setattr('requests.Session.post', mock_post)
    res = client.unlink_account(1234)
    assert res == {"result": "unlink account success"}
    assert mock_post.call_count == 1
    mock_post.assert_called_with(
        'https://graph.facebook.com/v{api_version}/me/unlink_accounts'.format(api_version=client.api_version),
        params=default_params,
        json={
            'psid': 1234,
        },
        timeout=None
    )


def test_add_whitelisted_domains(client, monkeypatch, default_params):
    mock_post = mock.Mock()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "result": "success",
    }
    monkeypatch.setattr('requests.Session.post', mock_post)
    res = client.update_whitelisted_domains(['https://facebook.com'])
    assert res == {"result": "success"}
    assert mock_post.call_count == 1
    mock_post.assert_called_with(
        'https://graph.facebook.com/v{api_version}/me/messenger_profile'.format(api_version=client.api_version),
        params=default_params,
        json={
            'whitelisted_domains': [
                'https://facebook.com',
            ],
        },
        timeout=None
    )


def test_add_whitelisted_domains_not_as_list(client, monkeypatch, default_params):
    mock_post = mock.Mock()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "result": "success",
    }
    monkeypatch.setattr('requests.Session.post', mock_post)
    res = client.update_whitelisted_domains('https://facebook.com')
    assert res == {"result": "success"}
    assert mock_post.call_count == 1
    mock_post.assert_called_with(
        'https://graph.facebook.com/v{api_version}/me/messenger_profile'.format(api_version=client.api_version),
        params=default_params,
        json={
            'whitelisted_domains': [
                'https://facebook.com',
            ],
        },
        timeout=None
    )


def test_remove_whitelisted_domains(client, monkeypatch, default_params):
    mock_post = mock.Mock()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "result": "success",
    }
    monkeypatch.setattr('requests.Session.delete', mock_post)
    res = client.remove_whitelisted_domains()
    assert res == {"result": "success"}
    assert mock_post.call_count == 1
    mock_post.assert_called_with(
        'https://graph.facebook.com/v{api_version}/me/messenger_profile'.format(api_version=client.api_version),
        params=default_params,
        json={
            'fields': [
                'whitelisted_domains',
            ],
        },
        timeout=None
    )


def test_upload_attachment(client, monkeypatch, default_params):
    mock_post = mock.Mock()
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "attachment_id": "12345",
    }
    monkeypatch.setattr('requests.Session.post', mock_post)

    attachment = attachments.Image(url='https://some-image.com/image.jpg')
    res = client.upload_attachment(attachment)
    assert res == {"attachment_id": "12345"}
    assert mock_post.call_count == 1
    mock_post.assert_called_with(
        'https://graph.facebook.com/v{api_version}/me/message_attachments'.format(api_version=client.api_version),
        params=default_params,
        json={
            'message': {
                'attachment': {
                    'type': 'image',
                    'payload': {
                        'url': 'https://some-image.com/image.jpg',
                    }
                }
            }
        },
        timeout=None
    )


def test_upload_url_required(client):
    attachment = attachments.Image(attachment_id='12345')
    with pytest.raises(ValueError):
        client.upload_attachment(attachment)


def test_upload_no_quick_replies(client):
    replies = quick_replies.QuickReplies(
        [quick_replies.QuickReply(title='hello', payload='hello')])
    attachment = attachments.Image(
        url='https://some-image.com/image.jpg', quick_replies=replies)
    with pytest.raises(ValueError):
        client.upload_attachment(attachment)


def test_default_session(client):
    assert isinstance(client.session, requests.Session)


def test_explicit_session():
    client = MessengerClient(12345678, session=mock.sentinel.session)
    assert client.session is mock.sentinel.session


def test_generate_appsecret_proof():
    client = MessengerClient('1595920652850039|OxHxLwLVJkTZhEjwlHqPgxKgzRVU', app_secret='2e82nk47smn29dnam298fnamq82')
    assert client.generate_appsecret_proof() == '577b294b975cde92b75ef73c1469c7355bd7fb5e568d522f534dc539dec65b38'


def test_auth_args_without_app_secret():
    client = MessengerClient(12345678)
    assert client.auth_args == {
        'access_token': 12345678,
    }


def test_auth_args_with_app_secret():
    client = MessengerClient('1595920652850039|OxHxLwLVJkTZhEjwlHqPgxKgzRVU', app_secret='2e82nk47smn29dnam298fnamq82')
    assert client.auth_args == {
        'access_token': '1595920652850039|OxHxLwLVJkTZhEjwlHqPgxKgzRVU',
        'appsecret_proof': '577b294b975cde92b75ef73c1469c7355bd7fb5e568d522f534dc539dec65b38',
    }
