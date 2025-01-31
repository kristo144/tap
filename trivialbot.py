from random import randint
from enum import Enum
from itertools import repeat
from mcpi import block

from bot import Bot

class TrivialBot(Bot):
    # Messages
    gameIntro = [
        "Welcome to TrivialBot",
        "The rules are these:",
        "1. You must pick a topic",
        "2. Then you will get a random question about the topic chosen",
        "3. If you answer correctly, you will have no problem",
        "4. If not, you will regret it :)"
        "If you wanna play, write 'Y', if not, write 'N'"
    ]

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

    class State(Enum):
        INIT    = 0
        CONFIRM = 1
        TOPIC   = 2
        ANSWER  = 3

    def __init__(self):
        super().__init__("TrivialBot")
        self.state = self.State.INIT
        
    def on_message(self, mc, msg):
        match self.state:
            case self.State.INIT:
                self.start_game(mc, msg)
            case self.State.CONFIRM:
                self.confirm_game(mc, msg)
            case self.State.TOPIC:
                self.get_topic(mc, msg)
            case self.State.ANSWER:
                self.get_answer(mc, msg)
            case _:
                raise ValueError("Invalid state")
            
    def start_game(self, mc, msg):
        list(map(self.say, repeat(mc), self.gameIntro))
        self.state = self.State.CONFIRM
        
    def confirm_game(self, mc, msg):
        match self.get_response(msg).upper():
            case "Y":
                self.say(mc, "Let's play!")
                self.state = self.State.TOPIC
                self.show_topics(mc)
            case "N":
                self.say(mc, "Okay, see you next time!")
                self.state = self.State.INIT
            case _:
                self.say(mc, "Please answer Y/N")
                
    def get_topic(self, mc, msg):
        response = self.get_response(msg)
        if response in self.topics:
            chosen_topic = self.topics[response]
            self.say(mc, f"You chose {chosen_topic}!")
            self.correct = self.ask_question(mc, chosen_topic)
            self.state = self.State.ANSWER
        else:
            self.show_topics(mc)
            
    def get_answer(self, mc, msg):
        response = self.get_response(msg)
        if response.lower() == self.correct.lower():
            self.say(mc, self.correctAnswer)
        else:
            self.handle_wrong_answer(mc)
        delattr(self, "correct")
        self.state = self.State.INIT
        
    def get_response(self, msg):
        return msg.message.replace("@"+self.get_name()+" ", '')
    
    def show_topics(self, mc):
        self.say(mc, "Choose a topic by typing its number:")
        list(map(lambda key: self.say(mc, f"{key}: {self.topics[key]}"), self.topics.keys()))     # Post to chat topics

    def ask_question(self, mc, topic):
        # Select and ask a random question.
        question, answer = self.questions[topic][randint(0, len(self.questions[topic]) - 1)]
        self.say(mc, question)
        return answer

    def handle_wrong_answer(self, mc):
        # Handle wrong answers.
        self.say(mc, self.wrongAnswer)
        player_pos = mc.player.getPos()
        mc.player.setPos(player_pos.x, player_pos.y + 30, player_pos.z)     # move player 30 blocks up
        mc.setBlock(player_pos.x, player_pos.y, player_pos.z, block.TNT.id)     # set TNT block (inactive)
        mc.setBlock(player_pos.x + 1, player_pos.y, player_pos.z, block.FIRE.id)    # ignite TNT block with fire block