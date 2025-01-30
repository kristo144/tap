from unittest.mock import MagicMock, patch
import unittest
from echobot import EchoBot

class TestEchoBot(unittest.TestCase):

    @patch("mcpi.minecraft.Minecraft")  # Simulate Minecraft connexion
    def test_on_message_echoes_back(self, mock_minecraft):
        # Simulate Minecraft instance
        mock_mc = MagicMock()
        mock_minecraft.return_value = mock_mc

        # Create EchoBot instance
        bot = EchoBot()

        # Simulate the say method
        bot.say = MagicMock()

        # Simulate receiving a message
        bot.on_message(mock_mc, MagicMock(message="Hello, EchoBot!"))

        # Check if say() was called with the expected message
        bot.say.assert_called_once_with(mock_mc, "Hello, EchoBot!")

if __name__ == "__main__":
    unittest.main()
