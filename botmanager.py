from time import sleep
from mcpi import minecraft
from itertools import repeat

from bot import Bot

class BotManager(object):
    __instance = None
    __interval = 1

    # Singleton
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(BotManager, cls).__new__(cls)
            cls.__bots = list()
            cls.__mc = minecraft.Minecraft.create()
        return cls.__instance
    
    def add_bot(self, bot):
        if not isinstance(bot, Bot):
            raise TypeError("Object must be a Bot")
        self.__bots.append(bot);
        
    def set_interval(self, interval):
        if not isinstance(interval, int):
            raise TypeError("Interval must be an int")
        if not interval > 0:
            raise ValueError("Interval must be greater than 0")
        self.__interval = interval
        
        
    def loop(self):
        while True:
            sleep(self.__interval)
            env = {}
            env["mc"] = self.__mc
            env["player"] = self.__mc.player
            env["messages"] = self.__mc.events.pollChatPosts()
            [ bot.execute_actions(env) for bot in self.__bots if bot.check_triggers(env) ]
            #[ bot.execute_actions(env) for bot, env in zip(self.__bots, repeat(environment)) if bot.check_triggers(env) ]