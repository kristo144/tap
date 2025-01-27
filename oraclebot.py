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
        self.add_trigger(lambda env: any(["@OracleBot" in msg.message for msg in env["messages"]]))
        self.add_action (lambda env: self.__post_answer(env))
        
    def __post_answer(self, env):
        i = randint(0, len(self.__answers) - 1)
        msg = "<OracleBot> " + self.__answers[i]
        env["mc"].postToChat(msg)