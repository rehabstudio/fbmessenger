import logging

import pytest

from fbmessenger import quick_replies
from fbmessenger.error_messages import CHARACTER_LIMIT_MESSAGE


class TestQuickReplies:

    def test_quick_reply(self):
        res = quick_replies.QuickReply(
            title='QR',
            payload='QR payload',
            image_url='QR image',
        )
        expected = {
            'content_type': 'text',
            'title': 'QR',
            'payload': 'QR payload',
            'image_url': 'QR image'
        }
        assert expected == res.to_dict()

    def test_quick_reply_title_too_long(self, caplog):
        with caplog.at_level(logging.WARNING, logger='fbmessenger.elements'):
            quick_replies.QuickReply(title='Title is over the 20 character limit',
                                           payload='QR payload')
            assert caplog.record_tuples == [
                ('fbmessenger.quick_replies', logging.WARNING,
                  CHARACTER_LIMIT_MESSAGE.format(field='Title', maxsize=20))]

    def test_quick_reply_payload_too_long(self):
        payload = 'x' * 1001
        with pytest.raises(ValueError) as err:
            quick_replies.QuickReply(title='QR', payload=payload)
        assert str(err.value) == 'Payload cannot be longer 1000 characters.'

    def test_quick_reply_invalid_type(self):
        with pytest.raises(ValueError) as err:
            quick_replies.QuickReply(title='QR', payload='test', content_type='wrong')
        assert str(err.value) == 'Invalid content_type provided.'

    def test_quick_replies(self):
        qr = quick_replies.QuickReply(title='QR', payload='QR payload')
        qrs = quick_replies.QuickReplies(quick_replies=[qr] * 2)
        expected = [
            {
                'content_type': 'text',
                'title': 'QR',
                'payload': 'QR payload'
            },
            {
                'content_type': 'text',
                'title': 'QR',
                'payload': 'QR payload'
            }
        ]
        assert expected == qrs.to_dict()

    def test_too_many_quick_replies(self):
        qr = quick_replies.QuickReply(title='QR', payload='QR payload')
        qr_list = [qr] * 12
        with pytest.raises(ValueError) as err:
            quick_replies.QuickReplies(quick_replies=qr_list)
        assert str(err.value) == 'You cannot have more than 10 quick replies.'
