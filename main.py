from Tobot import Tobot
from IRCInterpreter import IRCInterpreter

# Create a Tobot
# This will be passed to all Interpreters
# This lets them point there data to somewhere
tobot = Tobot()

# IRC Interpreter
# Will read commands sent to the bot in PRIVMSG format
IRCinterpreter = IRCInterpreter(tobot)