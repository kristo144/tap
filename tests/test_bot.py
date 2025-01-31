import unittest
from unittest.mock import MagicMock

from bot import Bot

class TestBot(unittest.TestCase):
    
    def test_name(self):
        name = "name"
        bot = Bot(name)
        self.assertEqual(bot.get_name(), name)
        
    def test_new_fail(self):
        self.assertRaises(TypeError, Bot, 123)
        
    def test_on_message(self):
        mc = MagicMock()
        bot = Bot("Test")
        bot.on_message(mc, None)
        mc.postToChat.assert_called_with("<Test> Hello!")
        
    def test_say(self):
        mc = MagicMock()
        bot = Bot("Test")
        bot.say(mc, "foo")
        mc.postToChat.assert_called_with("<Test> foo")