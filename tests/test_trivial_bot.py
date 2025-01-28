import pytest
from trivialBot.TrivialBot import send_message, ask_question

def test_send_message(mocker):
    # Mockea la función mc.postToChat
    mc = mocker.Mock()
    time.sleep(2)
    send_message(mc, "Hello, world!")
    mc.postToChat.assert_called_once_with("<TrivialBot> Hello, world!")

def test_ask_question(mocker):
    # Mockea el comportamiento de preguntas aleatorias
    mc = mocker.Mock()
    mocker.patch("TrivialBot.questions", {"Football": [("Test question?", "Answer")]})
    assert ask_question(mc, "Football") == "Answer"
