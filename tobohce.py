from echobot import Bot, EchoBot

def reverse_message(func):
    def wrapper(self, mc, msg):
        msg.message = "".join(reversed(msg.message))
        func(self, mc, msg)
    return wrapper

class toBohcE(EchoBot):
    def __init__(self):
        super().__init__()
        self._Bot__name = "toBohcE"
    
    @reverse_message
    def on_message(self, mc, msg):
        super().on_message(mc, msg)
        