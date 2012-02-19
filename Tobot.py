import socket
import re

ircRegex = r':((?P<USERNAME>[^!]+)!)?(?P<HOST>\S+)\s+(?P<ACTION>\S+)\s+:?(?P<CHANNEL>\S+)\s*(?:(?::|[+-]+)(?P<MESSAGE>.*))?'

class Tobot:
	def __init__(self):
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
						
						print 'Private Message for Tobot!'
						print 'From: {0}'.format(matches.group('USERNAME'))
						print 'Message: {0}'.format(matches.group('MESSAGE'))