class SenderAction(object):
    SENDER_ACTIONS = [
        'mark_seen',
        'typing_on',
        'typing_off'
    ]

    def __init__(self, sender_action):
        if sender_action not in self.SENDER_ACTIONS:
            raise ValueError('Invalid sender_action provided.')
        self.sender_action = sender_action

    def to_dict(self):
        return {
            'sender_action': self.sender_action
        }
