import pytest

from fbmessenger.sender_actions import SenderAction


class TestSenderActions:

    def test_mark_seen(self):
        res = SenderAction(sender_action='mark_seen')
        expected = {
            'sender_action': 'mark_seen'
        }
        assert expected == res.to_dict()

    def test_typing_on(self):
        res = SenderAction(sender_action='typing_on')
        expected = {
            'sender_action': 'typing_on'
        }
        assert expected == res.to_dict()

    def test_typing_off(self):
        res = SenderAction(sender_action='typing_off')
        expected = {
            'sender_action': 'typing_off'
        }
        assert expected == res.to_dict()

    def test_invalid_action(self):
        with pytest.raises(ValueError) as err:
            SenderAction(sender_action='invalid')
        assert str(err.value) == 'Invalid sender_action provided.'
