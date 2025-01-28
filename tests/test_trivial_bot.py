from unittest.mock import MagicMock, patch
import pytest
from trivialBot import send_message, get_user_response, ask_question, handle_wrong_answer, play_trivial, topics



@patch("mcpi.minecraft.Minecraft")              # Simulate Minecraft server
def test_bot_responds_to_tag(mock_minecraft):
    # Simulate Minecraft isntance
    mock_mc = MagicMock()
    mock_minecraft.return_value = mock_mc

    # Send message to chat
    send_message(mock_mc, "Test message")

    # Validate that bot has posted to chat expected message
    mock_mc.postToChat.assert_called_with("<TrivialBot> Test message")


