class Bot:
    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError
        self.__name = name
        
    def on_message(self, mc, msg):
        """Function to execute when the bot is mentioned"""
        self.say(mc, "Hello!")
    
    def get_name(self):
        return self.__name
    
    def say(self, mc, message):
        mc.postToChat("<" + self.__name + "> " + message)
