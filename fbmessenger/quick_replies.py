class QuickReply(object):

    def __init__(self, title, payload):
        if len(title) > 20:
            raise ValueError('Title cannot be longer 20 characters.')
        if len(payload) > 1000:
            raise ValueError('Payload cannot be longer 1000 characters.')

        self.title = title
        self.payload = payload

    def to_dict(self):
        return {
            'content_type': 'text',
            'title': self.title,
            'payload': self.payload
        }


class QuickReplies(object):
    def __init__(self, quick_replies):
        if len(quick_replies) > 10:
            raise ValueError('You cannot have more than 10 quick replies.')
        self.quick_replies = quick_replies

    def to_dict(self):
        return {
            'quick_replies': [
                quick_reply.to_dict() for quick_reply in self.quick_replies
            ]
        }
