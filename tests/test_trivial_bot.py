from unittest.mock import MagicMock, patch
import pytest
from trivialBot import send_message, get_user_response, ask_question, handle_wrong_answer, play_trivial, topics, gameIntro, playMessage



@patch("mcpi.minecraft.Minecraft")              # Simulate Minecraft server
def test_bot_responds_to_tag(mock_minecraft):
    # Simulate Minecraft instance
    mock_mc = MagicMock()
    mock_minecraft.return_value = mock_mc

    # Send message to chat
    send_message(mock_mc, "Test message")

    # Validate that bot has posted to chat expected message
    mock_mc.postToChat.assert_called_with("<TrivialBot> Test message")


@patch("mcpi.minecraft.Minecraft")
def test_bot_sends_intro_messages(mock_minecraft):
    # Simulate Minecraft instance
    mock_mc = MagicMock()
    mock_minecraft.return_value = mock_mc

    # Send introduction messages to chat
    for line in gameIntro:
        send_message(mock_mc, line)

    # Validate that bot has posted to chat expected message
    for line in gameIntro:
        mock_mc.postToChat.assert_any_call(f"<TrivialBot> {line}")


@patch("mcpi.minecraft.Minecraft")
def test_bot_responds_to_topic_choice(mock_minecraft):
    # Simulate Minecraft instance
    mock_mc = MagicMock()
    mock_minecraft.return_value = mock_mc

    # Simulate user response (football)
    user_response = "1"

    # Send topics messages to chat
    send_message(mock_mc, "Choose a topic by typing its number:")
    send_message(mock_mc, f"1: Football")
    topic_choice = user_response

    # Validate that bot has posted to chat expected topic message
    send_message(mock_mc, f"You chose {topics[topic_choice]}!")
    mock_mc.postToChat.assert_called_with("<TrivialBot> You chose Football!")


@patch("mcpi.minecraft.Minecraft")
def test_bot_responds_to_correct_answer(mock_minecraft):
    # Simulate Minecraft instance
    mock_mc = MagicMock()
    mock_minecraft.return_value = mock_mc

    # Simulate correct user response (France) to Football question
    correct_answer = "France"

    # Send football question to chat
    ask_question(mock_mc, "Football")

    # Simulate correct user response
    user_response = correct_answer
    send_message(mock_mc, f"Correct answer: {user_response}")

    # Validate that bot has posted to chat expected answer message
    mock_mc.postToChat.assert_called_with("<TrivialBot> Correct answer: France")

@patch("mcpi.minecraft.Minecraft")  # Mock de la conexión a Minecraft
@patch("mcpi.block")  # Mock del módulo block
def test_bot_responds_to_wrong_answer(mock_block, mock_minecraft):
    # Simulate Minecraft instance
    mock_mc = MagicMock()
    mock_minecraft.return_value = mock_mc

    # Simulate block
    mock_block.TNT.id = 46  # TNT ID
    mock_block.FIRE.id = 51  # Fire ID

    # Simulate wrong user answer
    handle_wrong_answer(mock_mc)

    # Validate that bot has posted to chat failed message
    mock_mc.postToChat.assert_any_call("<TrivialBot> Oh no, you failed the answer...")

    # Validate that player has been moved
    mock_mc.player.setPos.assert_called()

    # Obtain simulate player pos
    player_pos = mock_mc.player.getPos.return_value

    # Validate that TNT and Fire block are set
    mock_mc.setBlock.assert_any_call(player_pos.x, player_pos.y, player_pos.z, 46)  # TNT
    mock_mc.setBlock.assert_any_call(player_pos.x + 1, player_pos.y, player_pos.z, 51)  # Fire


@patch("mcpi.minecraft.Minecraft")
def test_bot_responds_to_play_decision(mock_minecraft):
    # Simulate Minecraft instance
    mock_mc = MagicMock()
    mock_minecraft.return_value = mock_mc

    # Simulate that user wants to play
    user_response = "Y"

    # Call function that waits user response
    send_message(mock_mc, playMessage)
    if user_response == "Y":
        send_message(mock_mc, "Let's play!")

    # Validate that bot has posted play message
    mock_mc.postToChat.assert_any_call("<TrivialBot> Let's play!")


@patch("mcpi.minecraft.Minecraft")
def test_bot_does_not_play(mock_minecraft):
    # Simulate Minecraft instance
    mock_mc = MagicMock()
    mock_minecraft.return_value = mock_mc

    # Simulate that user not wants to play
    user_response = "N"

    # Call function that waits user response
    send_message(mock_mc, playMessage)
    if user_response == "N":
        send_message(mock_mc, "Okay, see you next time!")

    # Validate that bot has posted not play message
    mock_mc.postToChat.assert_any_call("<TrivialBot> Okay, see you next time!")
