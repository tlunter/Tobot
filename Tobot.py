import socket
import re

ircRegex = r':((?P<USERNAME>[^!]+)!)?(?P<HOST>\S+)\s+(?P<ACTION>\S+)\s+:?(?P<CHANNEL>\S+)\s*(?:(?::|[+-]+)(?P<MESSAGE>.*))?'

class Tobot:
	def __init__(self, interpreter):
		
		self._interpreter = interpreter
		
		self._irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server = ('irc.freenode.net',6667)
		
		print 'Tobot Started'
		self._irc.connect(server)
		
		print 'Tobot Connected and Identifying'
		self._irc.send('NICK Tobot\r\n')
		self._irc.send('USER Tobot Tobot_ Tobot__ :Tobot\r\n')
		
		print 'Tobot Identified'
		self._irc.send('JOIN #326DVA\r\n')
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
				
						if matches.group('ACTION') == 'PRIVMSG' and matches.group('CHANNEL') == 'Tobot':
					
							print '\nPrivate Message for Tobot!'
							print 'From: {0}'.format(matches.group('USERNAME'))
							print 'Message: {0}\n'.format(matches.group('MESSAGE'))
					
							output = self._interpreter.interpret(matches.group('USERNAME'), matches.group('MESSAGE'))
					
							lines = output.split('\n')
					
							for line in lines:
						
								if line.strip() != '':
							
									privmsg = ':Tobot PRIVMSG {0} :{1}\r\n'.format(matches.group('USERNAME'),line)
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
			self._irc.send('QUIT :Lalala!\r\n')