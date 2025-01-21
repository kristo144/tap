from time import sleep
from random import randint
from mcpi import minecraft

botName="OracleBot"
botTag="@" + botName
botChat = "<" + botName + "> "

answers = [
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

mc = minecraft.Minecraft.create()

while True:
    sleep(2)
    msgs = mc.events.pollChatPosts()
    for msg in msgs:
        if botTag in msg.message:
            i = randint(0, len(answers))
            mc.postToChat(botChat + answers[i])
