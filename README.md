# Facebook Messenger

[![PyPI](https://img.shields.io/pypi/v/fbmessenger.svg?maxAge=2592000)](https://pypi.python.org/pypi/fbmessenger)
[![Build Status](https://travis-ci.org/rehabstudio/fbmessenger.svg?branch=master)](https://travis-ci.org/rehabstudio/fbmessenger)
[![Coverage Status](https://coveralls.io/repos/github/rehabstudio/fbmessenger/badge.svg?branch=master)](https://coveralls.io/github/rehabstudio/fbmessenger?branch=master)
[![PyPI](https://img.shields.io/pypi/l/fbmessenger.svg?maxAge=2592000)](https://pypi.python.org/pypi/fbmessenger)

A python library to communicate with the Facebook Messenger API's


## Installation

Install from pip

    pip install fbmessenger

## Facebook app setup

- [Create a page](https://www.facebook.com/pages/create/) for your app, if you don't already have one
- [Create an app](https://developers.facebook.com/quickstarts/?platform=web)
- Add the Messenger product
- Select the Page to generate a page token


## Example usage with Flask

First you need to create a verify token, this can be any string e.g. `'my_verify_token'`.


### Messenger class

We need to extend the `BaseMessenger` abstract class and implement methods for each of the following subscription fields.

- `messages`
- `message_deliveries`
- `message_reads`
- `messaging_optins`
- `messaging_postbacks`
- `account_linking`

```
from fbmessenger import BaseMessenger

class Messenger(BaseMessenger):
    def __init__(self, verify_token, page_access_token):
        self.page_access_token = page_access_token
        super(BaseMessenger, self).__init__(self.page_access_token)

    def messages(self, message):
        self.send({'text': 'Received: {0}'.format(message['message']['text'])})

    def message_deliveries(self, message):
        pass

    def message_reads(self, message):
        pass

    def account_linking(self, message):
        pass

    def messaging_postbacks(self, messages):
        pass

    def messaging_optins(self, messages):
        pass
```


### Create a route for the callback url

This can be used to process any messages received and also to verify your app

```
import os
from flask import Flask, request

app = Flask(__name__)

messenger = Messenger(os.environ.get('FB_VERIFY_TOKEN'), os.environ.get('FB_PAGE_TOKEN'))

@app.route('/webhook')
def webhook():
    if request.method == 'GET':
        if (request.args.get('hub.verify_token') == os.environ.get('FB_VERIFY_TOKEN')):
            return request.args.get('hub.challenge')
        raise ValueError('FB_VERIFY_TOKEN does not match.')
    elif request.method == 'POST':
        messenger.handle(request.get_json(force=True))
    return ''

if __name__ == "__main__":
    app.run(host='0.0.0.0')
```


## Elements

Import the elements (or just the ones you need)

`from fbmessenger import elements`

### Text

You can pass a simple dict  or use the Class

```
messenger.send({'text': msg})

elem = elements.Text('Your Message')
messenger.send(elem.to_dict())
```

### Web button

```
btn = elements.Button(title='Web button', url='http://example.com')
messenger.send(btn.to_dict())
```

### Payload button

To use these buttons you must have the `message_deliveries` subscription enabled

```
btn = elements.Button(title='Postback button', payload='payload')
messenger.send(btn.to_dict())
```

## Attachments

### Images

```
image = attachments.Image(url='http://example.com/image.jpg')
messenger.send(image.to_dict())
```

### Audio

```
audio = attachments.Image(url='http://example.com/audio.mp3')
messenger.send(audio.to_dict())
```

### Video

```
video = attachments.Video(url='http://example.com/video.mp4')
messenger.send(video.to_dict())
```

### Files

```
file = attachments.File(url='http://example.com/file.txt')
messenger.send(file.to_dict())
```

## Templates

Import the templates (or just the ones you need)

`from fbmessenger import templates`

### Generic template

```
btn = elements.Button(title='Web button', url='http://facebook.com')
elems = elements.Element(
    title='Element',
    item_url='http://facebook.com',
    image_url='http://facebook.com/image.jpg',
    subtitle='Subtitle',
    buttons=[
        btn
    ]
)
res = templates.GenericTemplate(elements=[elems])
messenger.send(res.to_dict())
```

### Button template

```
btn = elements.Button(title='Web button', url='http://facebook.com')
btn2 = elements.Button(title='Postback button', payload='payload')
res = templates.ButtonTemplate(
    text='Button template',
    buttons=[btn, btn2]
)
messenger.send(res.to_dict())
```

### Receipt template

```
element = elements.Element(
    title='Classic White T-Shirt',
    subtitle='100% Soft and Luxurious Cotton',
    quantity=2,
    price=50,
    currency='USD',
    image_url='http://petersapparel.parseapp.com/img/whiteshirt.png',
)
adjustment1 = elements.Adjustment(name='New Customer Discount', amount=20)
adjustment2 = elements.Adjustment(name='$10 Off Coupon', amount=10)
address = elements.Address(
    street_1='1 Hacker Way',
    city='Menlo Park',
    postal_code='94025',
    state='CA',
    country='US'
)
summary = elements.Summary(
    subtotal=75.00,
    shipping_cost=4.95,
    total_tax=6.19,
    total_cost=56.14
)
res = templates.ReceiptTemplate(
    recipient_name='Stephane Crozatier',
    order_number='12345678902',
    currency='USD',
    payment_method='Visa 2345',
    order_url='http://petersapparel.parseapp.com/order?order_id=123456',
    timestamp='1428444852',
    address=address,
    summary=summary,
    adjustments=[adjustment1, adjustment2],
    elements=[element]
)
messenger.send(res.to_dict())
```

## Sender Actions

### Typing on

```
typing_on = SenderAction(sender_action='typing_on')
messenger.send_action(typing_on.to_dict())
```

### Typing off

```
typing_ffn = SenderAction(sender_action='typing_off')
messenger.send_action(typing_off.to_dict())
```

### Mark seen

```
mark_seen = SenderAction(sender_action='mark_seen')
messenger.send_action(mark_seen.to_dict())
```

## Quick Replies

```
quick_reply_1 = QuickReply(title='Do something', payload='Send me this payload')
quick_reply_2 = QuickReply(title='Do something else', payload='Send me this other payload')
result = QuickReplies(quick_replies=[
	quick_reply_1,
	quick_reply_2
])
messenger.send(result.to_dict())
```

## Development Notes

[Pandoc](http://pandoc.org/installing.html) should be installed locally to convert the README to reStructuredText format for uploading to PyPi

### Creating a new release

Commit latest changes

```
git push --tags
python setup.py sdist bdist_wheel
twine upload -r pypi dist/fbmessenger-<version>*
```

