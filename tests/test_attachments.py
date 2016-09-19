import pytest

from fbmessenger import attachments
from fbmessenger import quick_replies


class TestAttachments:

    def test_image(self):
        res = attachments.Image(url='http://facebook.com/image.jpg')
        expected = {
            'attachment': {
                'type': 'image',
                'payload': {
                    'url': 'http://facebook.com/image.jpg'
                }
            }
        }
        assert expected == res.to_dict()

    def test_audio(self):
        res = attachments.Audio(url='http://facebook.com/audio.mp3')
        expected = {
            'attachment': {
                'type': 'audio',
                'payload': {
                    'url': 'http://facebook.com/audio.mp3'
                }
            }
        }
        assert expected == res.to_dict()

    def test_video(self):
        res = attachments.Video(url='http://facebook.com/video.mp4')
        expected = {
            'attachment': {
                'type': 'video',
                'payload': {
                    'url': 'http://facebook.com/video.mp4'
                }
            }
        }
        assert expected == res.to_dict()

    def test_file(self):
        res = attachments.File(url='http://facebook.com/file.txt')
        expected = {
            'attachment': {
                'type': 'file',
                'payload': {
                    'url': 'http://facebook.com/file.txt'
                }
            }
        }
        assert expected == res.to_dict()

    def test_quick_replies(self):
        qr = quick_replies.QuickReply(title='QR', payload='QR payload')
        qrs = quick_replies.QuickReplies(quick_replies=[qr] * 2)

        res = attachments.Image(
            url='http://facebook.com/image.jpg',
            quick_replies=qrs
        )
        expected = {
            'attachment': {
                'type': 'image',
                'payload': {
                    'url': 'http://facebook.com/image.jpg'
                },
            },
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
                },
            ],
        }
        assert expected == res.to_dict()

    def test_quick_replies_throws_error(self):
        with pytest.raises(ValueError) as err:
            attachments.Image(
                url='http://facebook.com/image.jpg',
                quick_replies='error'
            )
        assert str(err.value) == 'quick_replies must be an instance of QuickReplies.'

    def test_is_reusable(self):
        res = attachments.Image(
            url='http://facebook.com/image.jpg',
            is_reusable=True
        )
        expected = {
            'attachment': {
                'type': 'image',
                'payload': {
                    'url': 'http://facebook.com/image.jpg',
                    'is_reusable': 'true'
                }
            }
        }
        assert expected == res.to_dict()

    def test_attachment_id(self):
        res = attachments.Image(
            attachment_id=12345
        )
        expected = {
            'attachment': {
                'type': 'image',
                'payload': {
                    'attachment_id': 12345,
                }
            }
        }
        assert expected == res.to_dict()
