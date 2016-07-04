class BaseAttachment(object):
    def __init__(self, attachment_type, url):
        self.type = attachment_type
        self.url = url

    def to_dict(self):
        return {
            'attachment': {
                'type': self.type,
                'payload': {
                    'url': self.url
                }
            }
        }


class Image(BaseAttachment):
    def __init__(self, url):
        self.attachment_type = 'image'
        self.url = url
        super(Image, self).__init__(self.attachment_type, self.url)


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
