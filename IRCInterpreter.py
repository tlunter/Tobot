import socket
import re

# IRC Regex to catch raw data
ircRegex = r':((?P<USERNAME>[^!]+)!)?(?P<HOST>\S+)\s+(?P<ACTION>\S+)\s+:?(?P<CHANNEL>\S+)\s*(?:(?::|[+-]+)(?P<MESSAGE>.*))?'

# Default server and channel to join (I use the channel so I know the bot is online)
# Right now the bot does not respond if it sees it's name in the message
# Soon I will have it scrape the channel too
default_server = ('irc.freenode.net',6667)
default_channel = '#326DVA'

# The IRC Interpreter for the Tobot
class IRCInterpreter:
	def __init__(self, tobot):
		
		# Needs to know where to send the messages it receives
		self._tobot = tobot
		
		# Set up the IRC socket connection
		self._irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		# Connect to the IRC server
		print '{0} Started'.format(self._tobot.getName())
		self._irc.connect(default_server)
		
		# Send the identification information
		# Will set up a nickserv verification soon so the name is not taken
		print '{0} Connected and Identifying'.format(self._tobot.getName())
		self._irc.send('NICK {0}\r\n'.format(self._tobot.getName()))
		self._irc.send('USER {0} {0}_ {0}__ :Tobot\r\n'.format(self._tobot.getName()))
		
		# Joins the default channel
		print '{0} Identified'.format(self._tobot.getName())
		self._irc.send('JOIN {0}\r\n'.format(default_channel))
		print 'Attempting to join and start receiving data'
		
		# Time to start interpreting!
		self.startReceiving()
	
	# The only way and IRC bot can interpret is by forever reading the inputs
	def startReceiving(self):
		
		# Pre define oldData before the loop to catch information not with 4096 bytes
		oldData = ''
		
		# Used to capture keyboard interrupts and other exceptions
		try:
		
			# One continuous loop should work to get all data quickly
			while True:
				
				# newData is 4096 bytes of data max
				# Add the previous old data and then remove the last line of data
				# That line might be incomplete
				newData = self._irc.recv(4096)
				data = str(oldData) + str(newData)
				lines = data.split('\r\n')
				oldData = lines.pop()
				
				# Iterate through each raw line IRC data
				for line in lines:
					
					# If the server is pinging us to see our activity
					# Respond quickly
					checkPing = line.split()
					if checkPing[0] == 'PING':
				
						pongLine = 'PONG {0}\r\n'.format(checkPing[1])
						print pongLine
				
						self._irc.send(pongLine)
						continue
					
					# Now match the rest of the lines to then IRC regex
					# This will get the required groups and
					# make it easy to see what's happening
					matches = re.match(ircRegex, line)
			
					# If there are no matches, then there are no groups!
					if matches:
						
						# Redefines so that it's cleaner looking later on
						username = matches.group('USERNAME')
						host = matches.group('HOST')
						action = matches.group('ACTION')
						channel = matches.group('CHANNEL')
						message = matches.group('MESSAGE')
						
						# Currently just responds to private messages to the bot
						if action == 'PRIVMSG' and channel == self._tobot.getName():
						
							# A little bit of the raw read out of what the bot will interpret
							print '\nPrivate Message for {0}!'.format(self._tobot.getName())
							print 'From: {0}'.format(username)
							print 'Message: {0}\n'.format(message)
							output = self._tobot.interpret(username, message)
							
							# Splits the output into new lines so that it doesn't get prematurely called
							# and all data is sent
							lines = output.split('\n')
							
							for line in lines:
								
								# If no data, then why send anything?
								if line.strip() != '':
							
									# Send a private message back to who ever pm'd them in the first place
									privmsg = ':{0} PRIVMSG {1} :{2}\r\n'.format(self._tobot.getName(),username,line)
									print privmsg
							
									self._irc.send(privmsg)
									
		# If keyboard interrupted, just quit							
		except KeyboardInterrupt:
			self.quit()
			return
		
		# Otherwise quit gracefullly and print the exception
		except Exception, e:
			self.quit()
			print repr(e)
			return
			
	# Just sends the QUIT message so that the bot disconnects gracefully
	def quit(self):
			self._irc.send('QUIT :{0} Out!\r\n'.format(self._tobot.getName()))