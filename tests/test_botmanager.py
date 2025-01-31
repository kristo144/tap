import unittest
from unittest.mock import patch, MagicMock
import mcpi.block as block
from botmanager import BotManager, Bot

class TestBuilderBot(unittest.TestCase):

    @patch("mcpi.minecraft.Minecraft")
    def test_singleton(self, mock_mc):
        mgr = BotManager()
        mgr2 = BotManager()
        self.assertIs(mgr, mgr2)
        
    @patch("mcpi.minecraft.Minecraft")
    def test_add_bot_valid(self, mock_mc):
        mgr = BotManager()
        bot = Bot("Test")
        mgr.add_bot(bot)
        l = mgr._BotManager__bots
        self.assertIn(bot, l)
    
    @patch("mcpi.minecraft.Minecraft")
    def test_add_bot_fail(self, mock_mc):
        mgr = BotManager()
        self.assertRaises(TypeError, BotManager.add_bot, mgr, 123)
        
    @patch('mcpi.minecraft.Minecraft')
    def test_tick(self, mock_mc):
        mgr = BotManager()
        bot = MagicMock(spec=Bot)
        bot.get_name.return_value = "Name"
        mgr.add_bot(bot)
        
        msg = MagicMock()
        setattr(msg, "message", "@Name")
        mgr._BotManager__mc.events.pollChatPosts.return_value = [msg]
        mgr.tick()
        
        bot.get_name.assert_called_once()

    @patch('mcpi.minecraft.Minecraft')
    def test_manager_bot(self, mock_mc):
        mgr = BotManager()
        msg = MagicMock()
        setattr(msg, "message", "@ManagerBot")
        mgr._BotManager__mc.events.pollChatPosts.return_value = [msg]
        mgr.tick()
        mgr._BotManager__mc.postToChat.assert_any_call("<ManagerBot> The following bots are available:")