from random import randint

from bot import Bot

class OracleBot(Bot):
    __answers = [
        "It is certain",
        "Reply hazy, try again",
        "Don’t count on it",
        "It is decidedly so",
        "Ask again later",
        "My reply is no",
        "Without a doubt",
        "Better not tell you now",
        "My sources say no",
        "Yes definitely",
        "Cannot predict now",
        "Outlook not so good",
        "You may rely on it",
        "Concentrate and ask again",
        "Very doubtful",
        "As I see it, yes",
        "Most likely",
        "Outlook good",
        "Yes",
        "Signs point to yes",
    ]

    def __init__(self):
        super().__init__("OracleBot")
        
    def on_message(self, mc, msg):
        i = randint(0, len(self.__answers) - 1)
        self.say(mc, self.__answers[i])