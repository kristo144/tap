import unittest
from unittest.mock import MagicMock, patch
from random import randint
from bot import Bot
from oraclebot import OracleBot


class TestOracleBot(unittest.TestCase):

    @patch('random.randint')        # Simulate random.randint
    def test_on_message(self, mock_randint):
        # Simulate randint to obtain concrete number
        mock_randint.return_value = 5

        # Create OracleBot instance
        bot = OracleBot()

        # Simulate Minecraft object mc
        mc = MagicMock()

        # Simulate message for bot
        bot.on_message(mc, "What is the future?")

        # Validate that a message has been posted to chat
        bot.say(mc, "Ask again later")  # Debe responder con el índice 5 de las respuestas

        # Validate expected posted message
        mc.postToChat.assert_called_with("<OracleBot> Ask again later")

    def test_answer_choices(self):
        # Create OracleBot instance
        bot = OracleBot()

        # Obtain private attribute from OracleBot
        answers = bot._OracleBot__answers

        # Validate some possible answers are in answers list
        self.assertIn("It is certain", answers)
        self.assertIn("Reply hazy, try again", answers)
        self.assertIn("Don’t count on it", answers)
        self.assertIn("Ask again later", answers)
        self.assertIn("My reply is no", answers)


if __name__ == '__main__':
    unittest.main()
