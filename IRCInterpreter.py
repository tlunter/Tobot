import socket
import re

ircRegex = r':((?P<USERNAME>[^!]+)!)?(?P<HOST>\S+)\s+(?P<ACTION>\S+)\s+:?(?P<CHANNEL>\S+)\s*(?:(?::|[+-]+)(?P<MESSAGE>.*))?'
default_server = ('irc.freenode.net',6667)
default_channel = '#326DVA'

class IRCInterpreter:
	def __init__(self, tobot):
		
		self._tobot = tobot
		
		self._irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		print '{0} Started'.format(self._tobot.getName())
		self._irc.connect(default_server)
		
		print '{0} Connected and Identifying'.format(self._tobot.getName())
		self._irc.send('NICK {0}\r\n'.format(self._tobot.getName()))
		self._irc.send('USER {0} {0}_ {0}__ :Tobot\r\n'.format(self._tobot.getName()))
		
		print '{0} Identified'.format(self._tobot.getName())
		self._irc.send('JOIN {0}\r\n'.format(default_channel))
		print 'Attempting to join and start receiving data'
		
		self.startReceiving()
	
	def startReceiving(self):
		
		oldData = ''
	
		try:
		
			while True:
				
				newData = self._irc.recv(4096)
				data = str(oldData) + str(newData)
				lines = data.split('\r\n')
				oldData = lines.pop()
				
				for line in lines:
			
					checkPing = line.split()
					if checkPing[0] == 'PING':
				
						pongLine = 'PONG {0}\r\n'.format(checkPing[1])
						print pongLine
				
						self._irc.send(pongLine)
						continue
				
					matches = re.match(ircRegex, line)
			
					if matches:
						
						username = matches.group('USERNAME')
						host = matches.group('HOST')
						action = matches.group('ACTION')
						channel = matches.group('CHANNEL')
						message = matches.group('MESSAGE')
						
						if action == 'PRIVMSG' and channel == self._tobot.getName():
					
							print '\nPrivate Message for {0}!'.format(self._tobot.getName())
							print 'From: {0}'.format(username)
							print 'Message: {0}\n'.format(message)
							output = self._interpreter.interpret(username, message)
					
							lines = output.split('\n')
					
							for line in lines:
						
								if line.strip() != '':
							
									privmsg = ':{0} PRIVMSG {1} :{2}\r\n'.format(self._tobot.getName(),username,line)
									print privmsg
							
									self._irc.send(privmsg)
									
		except KeyboardInterrupt:
			self.quit()
			return
		except Exception, e:
			self.quit()
			print repr(e)
			return
			
	def quit(self):
			self._irc.send('QUIT :{0} Out!\r\n'.format(self._tobot.getName()))