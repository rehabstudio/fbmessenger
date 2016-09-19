from __future__ import absolute_import

from .quick_replies import QuickReplies


class BaseAttachment(object):
    def __init__(self, attachment_type, url=None, is_reusable=None,
                 quick_replies=None, attachment_id=None):
        self.attachment_type = attachment_type
        self.url = url
        self.is_reusable = is_reusable
        self.attachment_id = attachment_id

        if quick_replies and not isinstance(quick_replies, QuickReplies):
            raise ValueError('quick_replies must be an instance of QuickReplies.')
        self.quick_replies = quick_replies

    def to_dict(self):
        d = {
            'attachment': {
                'type': self.attachment_type,
                'payload': {}
            }
        }

        if self.url:
            d['attachment']['payload']['url'] = self.url

        if self.is_reusable:
            d['attachment']['payload']['is_reusable'] = 'true'

        if self.attachment_id:
            d['attachment']['payload']['attachment_id'] = self.attachment_id

        if self.quick_replies:
            d['quick_replies'] = self.quick_replies.to_dict()

        return d


class Image(BaseAttachment):
    def __init__(self, url=None, is_reusable=None, quick_replies=None, attachment_id=None):
        self.attachment_type = 'image'
        self.url = url
        self.is_reusable = is_reusable
        self.quick_replies = quick_replies
        self.attachment_id = attachment_id
        super(Image, self).__init__(self.attachment_type, self.url, self.is_reusable,
                                    self.quick_replies, self.attachment_id)


class Audio(BaseAttachment):
    def __init__(self, url=None, is_reusable=None, quick_replies=None, attachment_id=None):
        self.attachment_type = 'audio'
        self.url = url
        self.is_reusable = is_reusable
        self.quick_replies = quick_replies
        self.attachment_id = attachment_id
        super(Audio, self).__init__(self.attachment_type, self.url, self.is_reusable,
                                    self.quick_replies, self.attachment_id)


class Video(BaseAttachment):
    def __init__(self, url=None, is_reusable=None, quick_replies=None, attachment_id=None):
        self.attachment_type = 'video'
        self.url = url
        self.is_reusable = is_reusable
        self.quick_replies = quick_replies
        self.attachment_id = attachment_id
        super(Video, self).__init__(self.attachment_type, self.url, self.is_reusable,
                                    self.quick_replies, self.attachment_id)


class File(BaseAttachment):
    def __init__(self, url=None, is_reusable=None, quick_replies=None, attachment_id=None):
        self.attachment_type = 'file'
        self.url = url
        self.is_reusable = is_reusable
        self.quick_replies = quick_replies
        self.attachment_id = attachment_id
        super(File, self).__init__(self.attachment_type, self.url, self.is_reusable,
                                   self.quick_replies, self.attachment_id)
