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

# Create connection to Minecraft
mc = minecraft.Minecraft.create()

# Main loop
while True:
    sleep(2)
    msgs = mc.events.pollChatPosts()
    for msg in msgs:
        # Check if the bot is mentioned
        if botTag in msg.message:
            # Send intro and play message
            for line in gameIntro:
                mc.postToChat(botChat + line)
            mc.postToChat(botChat + playMessage)

            # Wait for response to play
            playing = False
            while not playing:
                sleep(1)
                responses = mc.events.pollChatPosts()
                for response in responses:
                    userResponse = response.message.strip().upper()  # Normalize message
                    if "Y" in userResponse:
                        mc.postToChat(botChat + "Let's play!")
                        playing = True
                        break
                    elif "N" in userResponse:
                        mc.postToChat(botChat + "Okay, see you next time!")
                        playing = True
                        break

            # If player wants to play
            if playing:
                # Show topics
                mc.postToChat(botChat + "Choose a topic by typing its number:")
                for key, topic in topics.items():
                    mc.postToChat(f"{key}: {topic}")

                chosenTopic = None
                while not chosenTopic:
                    sleep(1)
                    topic_msgs = mc.events.pollChatPosts()
                    for topic_msg in topic_msgs:
                        topicChoice = topic_msg.message.strip()
                        if topicChoice in topics:
                            chosenTopic = topics[topicChoice]
                            mc.postToChat(botChat + f"You chose {chosenTopic}!")
                            break

                # Pick a random question
                question, answer = questions[chosenTopic][randint(0, len(questions[chosenTopic]) - 1)]
                mc.postToChat(botChat + question)

                # Wait for the player's answer
                answered = False
                while not answered:
                    sleep(1)
                    answers_msgs = mc.events.pollChatPosts()
                    for answer_msg in answers_msgs:
                        playerAnswer = answer_msg.message.strip().lower()
                        if playerAnswer == answer.lower():
                            mc.postToChat(botChat + correctAnswer)
                            answered = True
                            break
                        else:
                            mc.postToChat(botChat + wrongAnswer)

                            # Move player up
                            playerPos = mc.player.getPos()
                            mc.player.setPos(playerPos.x, playerPos.y + 30, playerPos.z)

                            # Place TNT and fire below the player
                            mc.setBlock(playerPos.x, playerPos.y, playerPos.z, block.TNT.id)  # Place TNT
                            mc.setBlock(playerPos.x+1, playerPos.y, playerPos.z, block.FIRE.id)  # Ignite TNT

                            # Give TNT time to explode
                            sleep(4)

                            answered = True
                            break
