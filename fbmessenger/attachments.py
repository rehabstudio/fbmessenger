from __future__ import absolute_import

from .quick_replies import QuickReplies


class BaseAttachment(object):
    def __init__(self, attachment_type, url, is_reusable=None, quick_replies=None):
        self.type = attachment_type
        self.url = url

        if is_reusable is None:
            is_reusable = False
        self.is_reusable = is_reusable

        if quick_replies and not isinstance(quick_replies, QuickReplies):
            raise TypeError('quick_replies must be an instance of QuickReplies.')
        self.quick_replies = quick_replies

    def to_dict(self):
        d = {
            'attachment': {
                'type': self.type,
                'payload': {
                    'url': self.url
                }
            }
        }

        if self.is_reusable:
            d['attachment']['payload']['is_reusable'] = 'true'

        if self.quick_replies:
            d['attachment']['quick_replies'] = self.quick_replies.to_dict()

        return d


class Image(BaseAttachment):
    def __init__(self, url, quick_replies=None):
        self.attachment_type = 'image'
        self.url = url
        self.quick_replies = quick_replies
        super(Image, self).__init__(self.attachment_type, self.url, self.quick_replies)


class Audio(BaseAttachment):
    def __init__(self, url):
        self.attachment_type = 'audio'
        self.url = url
        super(Audio, self).__init__(self.attachment_type, self.url)


class Video(BaseAttachment):
    def __init__(self, url):
        self.attachment_type = 'video'
        self.url = url
        super(Video, self).__init__(self.attachment_type, self.url)


class File(BaseAttachment):
    def __init__(self, url):
        self.attachment_type = 'file'
        self.url = url
        super(File, self).__init__(self.attachment_type, self.url)
