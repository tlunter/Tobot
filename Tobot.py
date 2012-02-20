from PyPlugin import PyPlugin

class Tobot:
	
	def __init__(self, name = 'Tobot'):
		
		self._plugins = PyPlugin()
		self._name = name
		
	def getName(self):
		return self._name
	
	def interpret(self, username, input):
		
		inputSplit = input.split(None, 1)
		
		try:
			action = inputSplit[0]
		except IndexError:
			return ''
			
		try:
			data = inputSplit[1]
		except IndexError:
			data = ''
			
		output = ''
			
		for act, obj in self._plugins.getActionsAndObjects():
			
			if action == act:
				output = obj.sendInput(data)
				
		return output