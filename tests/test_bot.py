import unittest
from unittest.mock import MagicMock

from bot import Bot


class TestBot(unittest.TestCase):

    def test_name(self):
        """Ensure the bot returns the correct name."""
        name = "name"
        bot = Bot(name)
        self.assertEqual(bot.get_name(), name)

    def test_new_fail(self):
        """Check that creating a bot with an invalid name (non-string) raises a TypeError."""
        self.assertRaises(TypeError, Bot, 123)

    def test_on_message(self):
        """Verify that the bot responds correctly to a message event."""
        mc = MagicMock()
        bot = Bot("Test")
        bot.on_message(mc, None)

        # Ensure the bot sends the correct chat message
        mc.postToChat.assert_called_with("<Test> Hello!")

    def test_say(self):
        """Check if the bot correctly sends a custom message in chat."""
        mc = MagicMock()
        bot = Bot("Test")
        bot.say(mc, "foo")

        # Ensure the bot posts the expected chat message
        mc.postToChat.assert_called_with("<Test> foo")
