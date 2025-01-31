import unittest
from unittest.mock import patch, MagicMock
from botmanager import BotManager, Bot


class TestBotManager(unittest.TestCase):

    @patch("mcpi.minecraft.Minecraft")  # Simulate Minecraft connection
    def test_singleton(self):
        """Ensure BotManager follows the singleton pattern."""
        mgr = BotManager()
        mgr2 = BotManager()
        self.assertIs(mgr, mgr2)

    @patch("mcpi.minecraft.Minecraft")  # Simulate Minecraft connection
    def test_add_bot_valid(self):
        """Verify that a valid bot can be added to the manager."""
        mgr = BotManager()
        bot = Bot("Test")
        mgr.add_bot(bot)
        l = mgr._BotManager__bots
        self.assertIn(bot, l)

    @patch("mcpi.minecraft.Minecraft")  # Simulate Minecraft connection
    def test_add_bot_fail(self):
        """Ensure adding an invalid bot (non-Bot object) raises a TypeError."""
        mgr = BotManager()
        self.assertRaises(TypeError, BotManager.add_bot, mgr, 123)

    @patch('mcpi.minecraft.Minecraft')  # Simulate Minecraft connection
    def test_tick(self):
        """Check if tick() correctly processes chat messages for a bot."""
        mgr = BotManager()
        bot = MagicMock(spec=Bot)
        bot.get_name.return_value = "Name"
        mgr.add_bot(bot)

        # Simulate a chat event mentioning the bot
        msg = MagicMock()
        setattr(msg, "message", "@Name")
        mgr._BotManager__mc.events.pollChatPosts.return_value = [msg]
        mgr.tick()

        # Ensure get_name() was called at least once
        bot.get_name.assert_called_once()

    @patch('mcpi.minecraft.Minecraft')  # Simulate Minecraft connection
    def test_manager_bot(self):
        """Check if ManagerBot responds correctly to a command in chat."""
        mgr = BotManager()
        msg = MagicMock()
        setattr(msg, "message", "@ManagerBot")
        mgr._BotManager__mc.events.pollChatPosts.return_value = [msg]
        mgr.tick()

        # Ensure ManagerBot sends the correct response
        mgr._BotManager__mc.postToChat.assert_any_call("<ManagerBot> The following bots are available:")
