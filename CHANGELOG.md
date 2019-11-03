# Release History

## Unreleased
- Remove share button support (deprecated by Facebook)

## 6.0.0
- Switch from message to recipient_id as method input

## 5.6.1
- Update README
- remove pytest-catchlog from requirements.txt
- Add defaults for messaging_type & notification_type
- Add notification_type to BaseMessenger.send

## 5.6.0
- Adds app secret support

## 5.5.0
- Adds ability to set API version

## 5.4.0
- Allows specifying fields when requesting user data

## 5.3.2 
- Add missing tag parameter to BaseMessenger::send
- Remove invalid message tag

## 5.3.1 
- Adding 2 quick replies content_type: userphone_number, user_mail

## 5.3.0 
- Add share_contents support for share button

## 5.2.0
- The caller may now pass their own `requests.Session` object to
  `MessengerClient`. This is useful for eg. configuring retry behaviour.
- Every method that causes network access now accepts a `timeout`
  parameter.

## 5.1.0
- Add support for `notification_type` in the Send API.

## 5.0.0
- Breaking API change - `messaging_type` is now required when sending
  a message.

## 4.1.0

- Bring PersistentMenuItem up to date

## 4.0.1

- Add support for default_action to Element

## 4.0.0

- Support for new Messenger Profile

## 3.1.3

- Empty QuickReplies should evaluate to false

## 3.1.2

- Fixed quick replies in templates and attachments

## 3.1.1

- Added method to delete persistent menu

## 3.1.0

- Fixed quick replies, added location and images to quick replies
- Added webview and messenger extensions support
- Added reusable attachment support
- Can add and remove whitelisted domains
- element_share button support

## 3.0.1

- Added use of requests.Session for connection reuse

## 3.0.0

### Breaking changes

- Renamed abstract methods to match data structure
  Methods are now `message`, `delivery`, `optin`, `postback`, `read` and `account_linking`
- Renamed `subscribe` to `subscribe_app_to_page`

## 2.0.0
- Removed need for verify token when instanciating class
- Removed verify function
- Added callback account_linking webhook
- Support account_link and account_unlink button types
- Message echoes removed, should be handled in messages callback and checking for `"is_echo": "true"`
- Added delete_thread_setting method

## 1.1.0
- Added `BaseMessenger#send_actions` method

## 1.0.0

### Breaking changes

- `Elements#Image` moved to `Attachments#Image`
- `MessengerClient#send_data` renamed to `send`
- `MessengerClient#set_welcome_message removed`
- `BaseMessenger#message_echoes` and `BaseMessenger#message_reads` handlers now required
- Buttons now require a `button_type` parameter


### New features

- Support for audio, video and file attachments
- Support for sender actions
- Support for quick replies
- Support for get started button and persistent menus
- locale, timezone and gender now returned for user
- Support for phone_number button types
