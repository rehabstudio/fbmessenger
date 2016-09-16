import os

from flask import Flask, request
from fbmessenger import BaseMessenger
from fbmessenger.templates import GenericTemplate
from fbmessenger.elements import Text, Button, Element
from fbmessenger import quick_replies
from fbmessenger.attachments import Image, Video
from fbmessenger.thread_settings import (
    GreetingText,
    GetStartedButton,
    PersistentMenuItem,
    PersistentMenu,
)


def get_button(ratio):
    return Button(
        button_type='web_url',
        title='facebook {}'.format(ratio),
        url='https://facebook.com/',
        webview_height_ratio=ratio,
    )


def get_element(btn):
    return Element(
        title='Testing template',
        item_url='http://facebook.com',
        image_url='http://placehold.it/300x300',
        subtitle='Subtitle',
        buttons=[btn]
    )


def process_message(message):
    app.logger.debug('Message received: {}'.format(message))

    if 'attachments' in message['message']:
        if message['message']['attachments'][0]['type'] == 'location':
            app.logger.debug('Location received')
            response = Text(text='{}: lat: {}, long: {}'.format(
                message['message']['attachments'][0]['title'],
                message['message']['attachments'][0]['payload']['coordinates']['lat'],
                message['message']['attachments'][0]['payload']['coordinates']['long']
            ))
            return response.to_dict()

    if 'text' in message['message']:
        msg = message['message']['text'].lower()
        response = Text(text='Sorry didn\'t understand that: {}'.format(msg))
        if 'text' in msg:
            response = Text(text='This is an example text message.')
        if 'image' in msg:
            response = Image(url='https://unsplash.it/300/200/?random')
        if 'video' in msg:
            response = Video(url='http://techslides.com/demos/sample-videos/small.mp4')
        if 'quick replies' in msg:
            qr1 = quick_replies.QuickReply(title='Location', content_type='location')
            qr2 = quick_replies.QuickReply(title='Payload', payload='QUICK_REPLY_PAYLOAD')
            qrs = quick_replies.QuickReplies(quick_replies=[qr1, qr2])
            response = Text(text='This is an example text message.', quick_replies=qrs)
        if 'payload' in msg:
            txt = 'User clicked {}, button payload is {}'.format(
                msg,
                message['message']['quick_reply']['payload']
            )
            response = Text(text=txt)
        if 'webview-compact' in msg:
            btn = get_button(ratio='compact')
            elem = get_element(btn)
            response = GenericTemplate(elements=[elem])
        if 'webview-tall' in msg:
            btn = get_button(ratio='tall')
            elem = get_element(btn)
            response = GenericTemplate(elements=[elem])
        if 'webview-full' in msg:
            btn = get_button(ratio='full')
            elem = get_element(btn)
            response = GenericTemplate(elements=[elem])

        return response.to_dict()


class Messenger(BaseMessenger):
    def __init__(self, page_access_token):
        self.page_access_token = page_access_token
        super(Messenger, self).__init__(self.page_access_token)

    def message(self, message):
        action = process_message(message)
        res = self.send(action)
        app.logger.debug('Response: {}'.format(res))

    def delivery(self, message):
        pass

    def read(self, message):
        pass

    def account_linking(self, message):
        pass

    def postback(self, message):
        payload = message['postback']['payload']
        if 'start' in payload:
            txt = ('Hey, let\'s get started! Try sending me one of these messages: '
                   'text, image, video, "quick replies", '
                   'webview-compact, webview-tall, webview-full')
            self.send({'text': txt})
        if 'help' in payload:
            self.send({'text': 'A help message or template can go here.'})

    def optin(self, message):
        pass

    def init_bot(self):
        self.add_whitelisted_domains('https://facebook.com/')
        greeting = GreetingText(text='Welcome to the fbmessenger bot demo.')
        self.set_thread_setting(greeting.to_dict())

        get_started = GetStartedButton(payload='start')
        self.set_thread_setting(get_started.to_dict())

        menu_item_1 = PersistentMenuItem(
            item_type='postback',
            title='Help',
            payload='help',
        )
        menu_item_2 = PersistentMenuItem(
            item_type='web_url',
            title='Messenger Docs',
            url='https://developers.facebook.com/docs/messenger-platform',
        )
        persistent_menu = PersistentMenu(menu_items=[
            menu_item_1,
            menu_item_2
        ])

        res = self.set_thread_setting(persistent_menu.to_dict())
        app.logger.debug('Response: {}'.format(res))


app = Flask(__name__)
app.debug = True
messenger = Messenger(os.environ.get('FB_PAGE_TOKEN'))


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == os.environ.get('FB_VERIFY_TOKEN'):
            if request.args.get('init') and request.args.get('init') == 'true':
                messenger.init_bot()
                return ''
            return request.args.get('hub.challenge')
        raise ValueError('FB_VERIFY_TOKEN does not match.')
    elif request.method == 'POST':
        messenger.handle(request.get_json(force=True))
    return ''


if __name__ == '__main__':
    app.run(host='0.0.0.0')
