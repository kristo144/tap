from time import sleep
from mcpi import minecraft

from bot import Bot

class BotManager(object):
    __instance = None

    # Singleton
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(BotManager, cls).__new__(cls)
            cls.__bots = list()
            cls.__bots.append(ManagerBot(cls.__bots))
            cls.__mc = minecraft.Minecraft.create()
        return cls.__instance
    
    def add_bot(self, bot):
        if not isinstance(bot, Bot):
            raise TypeError("Object must be a Bot")
        self.__bots.append(bot)
        
    def tick(self):
        msgs = self.__mc.events.pollChatPosts()
        [ bot.on_message(self.__mc, msg)
         for bot in self.__bots
         for msg in msgs
         if "@" + bot.get_name() in msg.message ]

    def loop(self):
        while True:
            sleep(1)
            self.tick()
            
class ManagerBot(Bot):
    def __init__(self, bots):
        super().__init__("ManagerBot")
        self.__bots = bots
        
    def on_message(self, mc, msg):
        self.say(mc, "The following bots are available:")
        [ self.say(mc, bot.get_name()) for bot in self.__bots ]