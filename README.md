# fbmessenger

![https://travis-ci.com/rehabstudio/fbmessenger.svg?token=GC74DPVqhupkfZm2TAsz&branch=master](https://travis-ci.com/rehabstudio/fbmessenger.svg?token=GC74DPVqhupkfZm2TAsz&branch=master)

A python library to integrate with Facebook Messenger


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

We need to extend the `BaseMessenger` class and def methods for each of the subscription fields you want to handle.

- `messages`
- `message_deliveries`
- `messaging_optins`
- `messaging_postbacks`

For simple bots you can just select the `messages` field

To process `message_deliveries` you would need to define a `message_deliveries` method on the class to handle this message type. The same applies for the other message types

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

### Elements
Elements can be used in the generic templates

```
btn = elements.Button(title='Buy now', url='http://example.com')
elem = elements.Element(
    title='Green T-shirt',
    item_url='http://example.com',
    image_url='http://example.com/image.jpg',
    subtitle='100% cotton',
    buttons=[
        btn
    ]
)
```
## Templates

## References

This library is a basic port of the ideas from [justynjozwiak/messenger-wrapper](https://github.com/justynjozwiak/messenger-wrapper)

## How to Contribute

- Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
- Fork [the repository](http://github.com/rehabstudio/fbmessenger) on GitHub to start making your changes to the **master** branch (or branch off of it).
- Write a test which shows that the bug was fixed or that the feature works as expected.
- Send a pull request and bug the maintainer until it gets merged and published.
