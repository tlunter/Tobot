from PyPlugin import PyPlugin

class Interpreter:
	
	def __init__(self):
		
		self._plugins = PyPlugin()
	
	def interpret(self, username, input):
		
		interpretation = input.split(None, 1)
		
		try:
			action = interpretation[0]
		except IndexError:
			return ''
			
		try:
			data = interpretation[1]
		except IndexError:
			data = ''
			
		output = ''
			
		for act, obj in self._plugins.getActionsAndObjects():
			
			if action == act:
				output = obj.sendInput(data)
				
		return output