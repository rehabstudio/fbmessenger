from fbmessenger import attachments


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
