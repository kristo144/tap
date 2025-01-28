import unittest
from unittest.mock import MagicMock, patch
from oraclebot import process_messages, botTag, botChat, answers


class TestOracleBot(unittest.TestCase):
    @patch("mcpi.minecraft.Minecraft")             # Simulate Minecraft server
    def test_bot_responds_to_tag(self, mock_minecraft):
        # Simulate Minecraft client
        mc = mock_minecraft.create.return_value

        # Simulate message tagging bot
        mc.events.pollChatPosts.return_value = [
            MagicMock(message=f"{botTag} Will I win?")
        ]

        # Call function that processes messages
        process_messages(mc)

        # Validate that bot has post to chat
        mc.postToChat.assert_called()

        # Obtain sent message
        sent_message = mc.postToChat.call_args[0][0]

        # Validate expected response
        self.assertTrue(any(sent_message.endswith(answer) for answer in answers))

    @patch("mcpi.minecraft.Minecraft")             # Simulate Minecraft server
    def test_bot_ignores_unrelated_messages(self, mock_minecraft):
        # Simulate Minecraft client
        mc = mock_minecraft.create.return_value

        # Simulate message not tagging bot
        mc.events.pollChatPosts.return_value = [
            MagicMock(message="Hello there!")
        ]

        # Call function that processes messages
        process_messages(mc)

        # Validate that bot has not posted to chat
        mc.postToChat.assert_not_called()

    @patch("mcpi.minecraft.Minecraft")             # Simulate Minecraft server
    def test_bot_message_format(self, mock_minecraft):
        # Simulate Minecraft client
        mc = mock_minecraft.create.return_value

        # Simulate message tagging bot
        mc.events.pollChatPosts.return_value = [
            MagicMock(message=f"{botTag} Should I do it?")
        ]

        # Call function that processes messages
        process_messages(mc)

        # Obtain sent message
        sent_message = mc.postToChat.call_args[0][0]

        # Validate expected message format
        self.assertTrue(sent_message.startswith(botChat))
        self.assertIn(sent_message[len(botChat):], answers)

    @patch("mcpi.minecraft.Minecraft")             # Simulate Minecraft server
    def test_bot_handles_no_messages(self, mock_minecraft):
        # Simulate Minecraft client
        mc = mock_minecraft.create.return_value

        # Simulate that are no messages
        mc.events.pollChatPosts.return_value = []

        # Call function that processes messages
        process_messages(mc)

        # Validate that bot has not posted to chat
        mc.postToChat.assert_not_called()


if __name__ == "__main__":
    unittest.main()
