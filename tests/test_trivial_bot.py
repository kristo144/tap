import unittest
from unittest.mock import MagicMock, patch
from random import randint
from mcpi.vec3 import Vec3

from trivialbot import TrivialBot

class TestTrivialBot(unittest.TestCase):

    def test_state_init(self):
        """Ensure the bot starts in INIT state and transitions to CONFIRM after a message."""
        mc = MagicMock()
        bot = TrivialBot()
        bot.on_message(mc, None)
        mc.postToChat.assert_called()
        self.assertEqual(bot.state, TrivialBot.State.CONFIRM)

    def test_deny_game(self):
        """Verify that responding with 'N' cancels the game and resets the state to INIT."""
        mc = MagicMock()
        msg = MagicMock()
        msg.message = "N"
        bot = TrivialBot()
        bot.state = TrivialBot.State.CONFIRM
        bot.on_message(mc, msg)
        mc.postToChat.assert_called()
        self.assertEqual(bot.state, TrivialBot.State.INIT)

    def test_accept_game(self):
        """Ensure that responding with 'Y' moves the bot to the TOPIC selection state."""
        mc = MagicMock()
        msg = MagicMock()
        msg.message = "Y"
        bot = TrivialBot()
        bot.state = TrivialBot.State.CONFIRM
        bot.on_message(mc, msg)
        mc.postToChat.assert_called()
        self.assertEqual(bot.state, TrivialBot.State.TOPIC)

    def test_retry_confirm(self):
        """Check that an invalid response keeps the bot in the CONFIRM state."""
        mc = MagicMock()
        msg = MagicMock()
        msg.message = "foobar"
        bot = TrivialBot()
        bot.state = TrivialBot.State.CONFIRM
        bot.on_message(mc, msg)
        mc.postToChat.assert_called()
        self.assertEqual(bot.state, TrivialBot.State.CONFIRM)

    def test_invalid_topic(self):
        """Ensure that selecting an invalid topic does not change the state."""
        mc = MagicMock()
        msg = MagicMock()
        msg.message = "5"
        bot = TrivialBot()
        bot.state = TrivialBot.State.TOPIC
        bot.on_message(mc, msg)
        mc.postToChat.assert_any_call("<TrivialBot> Choose a topic by typing its number:")
        self.assertEqual(bot.state, TrivialBot.State.TOPIC)

    @patch('trivialbot.randint')
    def test_valid_topic(self, mock_randint):
        """Check if selecting a valid topic moves the bot to the ANSWER state."""
        mock_randint.return_value = 0
        mc = MagicMock()
        msg = MagicMock()
        msg.message = "2"
        bot = TrivialBot()
        bot.state = TrivialBot.State.TOPIC
        bot.on_message(mc, msg)
        mc.postToChat.assert_any_call("<TrivialBot> What is the chemical symbol for water? (Answer with a symbol)")
        self.assertEqual(bot.state, TrivialBot.State.ANSWER)
        self.assertEqual(bot.correct, "H2O")

    def test_right_answer(self):
        """Ensure that answering correctly resets the bot's state and removes the answer reference."""
        mc = MagicMock()
        ans = "foobar"
        msg = MagicMock()
        msg.message = ans
        bot = TrivialBot()
        bot.state = TrivialBot.State.ANSWER
        bot.correct = ans
        bot.on_message(mc, msg)
        mc.postToChat.assert_any_call("<TrivialBot> Congratulations!")
        self.assertEqual(bot.state, TrivialBot.State.INIT)
        self.assertFalse(hasattr(bot, "correct"))

    def test_wrong_answer(self):
        """Check if a wrong answer causes the bot to reset and teleport the player."""
        mc = MagicMock()
        mc.player.getPos.return_value = Vec3(0, 0, 0)
        msg = MagicMock()
        msg.message = "not correct"
        bot = TrivialBot()
        bot.state = TrivialBot.State.ANSWER
        bot.correct = "correct"
        bot.on_message(mc, msg)
        mc.postToChat.assert_any_call("<TrivialBot> Oh no, you failed the answer...")
        self.assertEqual(bot.state, TrivialBot.State.INIT)
        self.assertFalse(hasattr(bot, "correct"))
        mc.player.setPos.assert_called_with(0, 30, 0)  # Player should be teleported up

    def test_invalid_state(self):
        """Ensure that an invalid state raises a ValueError."""
        bot = TrivialBot()
        bot.state = 5  # Invalid state
        self.assertRaises(ValueError, TrivialBot.on_message, bot, None, None)

    def test_bot_sends_intro_messages(self):
        """Check that the bot sends introductory messages when a game starts."""
        mc = MagicMock()
        bot = TrivialBot()
        bot.on_message(mc, None)

        # Validate that bot has posted to chat expected message
        map(mc.postToChat.assert_any_call,
            map(lambda line: f"<TrivialBot> {line}", bot.gameIntro))
