
action = 'tP'

class testPlugin:
	
	def sendInput(self, data):
		
		if data == '':
			
			return 'You didn\'t input anything :('
			
		else:
			
			return 'You inputted: ' + data
		
		
testPlugin = testPlugin()