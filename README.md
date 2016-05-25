# Facebook Messenger

[![PyPI](https://img.shields.io/pypi/v/fbmessenger.svg?maxAge=2592000)](https://pypi.python.org/pypi/fbmessenger)
![https://travis-ci.com/rehabstudio/fbmessenger.svg?token=GC74DPVqhupkfZm2TAsz&branch=master](https://travis-ci.com/rehabstudio/fbmessenger.svg?token=GC74DPVqhupkfZm2TAsz&branch=master)
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

We need to extend the `BaseMessenger` class and implement methods for each of the following subscription fields.

- `messages`
- `message_deliveries`
- `messaging_optins`
- `messaging_postbacks`

```
from fbmessenger import BaseMessenger

class Messenger(BaseMessenger):
    def __init__(self, verify_token, page_access_token):
        self.verify_token = verify_token
        self.page_access_token = page_access_token
        super(BaseMessenger, self).__init__(self.verify_token,
                                            self.page_access_token)

    def messages(self, message):
        self.send({'text': 'Received: {0}'.format(message['message']['text'])})

    def message_deliveries(self, message):
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
        return messenger.verify(request.args.get('hub.verify_token'), request.args.get('hub.challenge'))
    elif request.method == 'POST':
        messenger.handle(request.get_json(force=True))
    return ''

if __name__ == "__main__":
    app.run(host='0.0.0.0')
```


## Elements

`from fbmessenger import elements`

### Text

You can pass a simple dict  or use the Class

```
messenger.send({'text': msg})

elem = elements.Text('Your Message')
messenger.send(elem.to_dict())
```

### Images

```
image = elements.Image(url='http://example.com/image.jpg')
messenger.send(image.to_dict())
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

## Development Notes

[Pandoc](http://pandoc.org/installing.html) should be installed locally to convert the README to reStructuredText format for uploading to PyPi
