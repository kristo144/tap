from random import randint
from time import sleep
from mcpi import minecraft, block

# Bot configuration
botName = "TrivialBot"
botTag = "@" + botName
botChat = "<" + botName + "> "

# Messages
gameIntro = [
    "Welcome to TrivialBot",
    "The rules are these:",
    "1. You must pick a topic",
    "2. Then you will get a random question about the topic chosen",
    "3. If you answer correctly, you will have no problem",
    "4. If not, you will regret it :)"
]
playMessage = "If you wanna play, write 'Y', if not, write 'N'"

topics = {
    "1": "Football",
    "2": "Science",
    "3": "Movies",
    "4": "Geography"
}

questions = {
    "Football": [
        ("How many champions does Luka Modric have? (Answer with a number)", "5"),
        ("Is Barça FC better than Real Madrid FC? (Answer with 'Yes' or 'No')", "No"),
        ("Which country won the FIFA World Cup in 2018? (Answer with a country name)", "France"),
        ("Who is the top scorer in UEFA Champions League history? (Answer with a name)", "Cristiano Ronaldo"),
        ("Which team has won the most La Liga titles? (Answer with a team name)", "Real Madrid")
    ],
    "Science": [
        ("What is the chemical symbol for water? (Answer with a symbol)", "H2O"),
        ("What planet is known as the Red Planet? (Answer with a name)", "Mars"),
        ("What is the speed of light? (Answer in km/s)", "300000"),
        ("Who developed the theory of relativity? (Answer with a name)", "Einstein"),
        ("What is the powerhouse of the cell? (Answer with an organelle name)", "Mitochondria")
    ],
    "Movies": [
        ("Who directed the movie 'Inception'? (Answer with a name)", "Christopher Nolan"),
        ("Which movie won the Oscar for Best Picture in 2020? (Answer with a title)", "Parasite"),
        ("Who played Iron Man in the Marvel movies? (Answer with a name)", "Robert Downey Jr."),
        ("What is the highest-grossing film of all time? (Answer with a title)", "Avatar"),
        ("Which movie franchise features a character named 'John Wick'? (Answer with a title)", "John Wick")
    ],
    "Geography": [
        ("What is the capital of France? (Answer with a city name)", "Paris"),
        ("Which country has the largest population? (Answer with a country name)", "China"),
        ("What is the longest river in the world? (Answer with a name)", "Nile"),
        ("Which desert is the largest in the world? (Answer with a name)", "Sahara"),
        ("What is the tallest mountain in the world? (Answer with a name)", "Everest")
    ]
}

correctAnswer = "Congratulations!"
wrongAnswer = "Oh no, you failed the answer..."


# Functional helpers
send_message = lambda mc, message: mc.postToChat(botChat + message)
get_user_response = lambda mc: next((msg.message.strip() for msg in mc.events.pollChatPosts()), None)
filter_messages = lambda mc, cond: list(filter(cond, mc.events.pollChatPosts()))


def ask_question(mc, topic):
    # Select and ask a random question.
    question, answer = questions[topic][randint(0, len(questions[topic]) - 1)]
    send_message(mc, question)
    return answer


def handle_wrong_answer(mc):
    # Handle wrong answers.
    send_message(mc, wrongAnswer)
    player_pos = mc.player.getPos()
    mc.player.setPos(player_pos.x, player_pos.y + 30, player_pos.z)     # move player 30 blocks up
    mc.setBlock(player_pos.x, player_pos.y, player_pos.z, block.TNT.id)     # set TNT block (inactive)
    mc.setBlock(player_pos.x + 1, player_pos.y, player_pos.z, block.FIRE.id)    # ignite TNT block with fire block
    sleep(4)


def play_trivial(mc):
    # Main game logic

    # Send intro messages
    list(map(lambda line: send_message(mc, line), gameIntro))
    send_message(mc, playMessage)

    # Wait for the player's decision
    while True:
        response = get_user_response(mc)
        if response is None:
            continue                        # Wait for messages if no response
        response = response.upper()         # Normalize response
        if response == "Y":
            send_message(mc, "Let's play!")
            break
        elif response == "N":
            send_message(mc, "Okay, see you next time!")
            return

    # Let the player choose a topic
    send_message(mc, "Choose a topic by typing its number:")
    list(map(lambda key: send_message(mc, f"{key}: {topics[key]}"), topics.keys()))     # Post to chat topics

    topic_choice = None
    while topic_choice not in topics:
        topic_choice = get_user_response(mc)                # Get user's topic choice

    chosen_topic = topics[topic_choice]
    send_message(mc, f"You chose {chosen_topic}!")

    # Ask a question about chosen topic
    correct_answer = ask_question(mc, chosen_topic)

    # Wait for player's answer
    while True:
        player_answer = get_user_response(mc)
        if player_answer is None:
            continue                                            # Wait for messages if no response
        if player_answer.lower() == correct_answer.lower():     # Normalize response
            send_message(mc, correctAnswer)
            break
        else:
            handle_wrong_answer(mc)
            break


# Main loop
if __name__ == "__main__":

    # Create connection to Minecraft
    mc = minecraft.Minecraft.create()

    sleep(2)
    messages = filter_messages(mc, lambda msg: botTag in msg.message)       # find botTag in chat
    if messages:
        play_trivial(mc)
