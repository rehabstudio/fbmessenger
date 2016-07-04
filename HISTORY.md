# Release History

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
