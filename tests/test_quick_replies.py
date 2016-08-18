import pytest

from fbmessenger import quick_replies


class TestQuickReplies:

    def test_quick_reply(self):
        res = quick_replies.QuickReply(title='QR', payload='QR payload')
        expected = {
            'content_type': 'text',
            'title': 'QR',
            'payload': 'QR payload'
        }
        assert expected == res.to_dict()

    def test_quick_reply_title_too_long(self):
        with pytest.raises(ValueError) as err:
            quick_replies.QuickReply(title='Title is over the 20 character limit',
                                           payload='QR payload')
        assert str(err.value) == 'Title cannot be longer 20 characters.'

    def test_quick_reply_payload_too_long(self):
        payload = 'x' * 1001
        with pytest.raises(ValueError) as err:
            quick_replies.QuickReply(title='QR',
                                           payload=payload)
        assert str(err.value) == 'Payload cannot be longer 1000 characters.'

    def test_quick_replies(self):
        qr = quick_replies.QuickReply(title='QR', payload='QR payload')
        res = quick_replies.QuickReplies(quick_replies=[qr] * 2)
        expected = {
            'quick_replies': [
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
        }
        assert expected == res.to_dict()

    def test_too_many_quick_replies(self):
        qr = quick_replies.QuickReply(title='QR', payload='QR payload')
        qr_list = [qr] * 11
        with pytest.raises(ValueError) as err:
            quick_replies.QuickReplies(quick_replies=qr_list)
        assert str(err.value) == 'You cannot have more than 10 quick replies.'
