from bot import Bot

class EchoBot(Bot):
    def __init__(self):
        super().__init__("EchoBot")
        
    def on_message(self, mc, msg):
        self.say(mc, msg.message)