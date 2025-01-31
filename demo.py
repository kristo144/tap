from botmanager import BotManager
from oraclebot import OracleBot
from echobot import EchoBot
from builderbot import BuilderBot
from trivialbot import TrivialBot
from tobohce import toBohcE

mgr = BotManager()
mgr.add_bot(OracleBot())
mgr.add_bot(EchoBot())
mgr.add_bot(BuilderBot())
mgr.add_bot(TrivialBot())
mgr.add_bot(toBohcE())
mgr.loop()