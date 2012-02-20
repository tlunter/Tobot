import sys
import os
import imp

class PyPlugin:

	def __init__(self, pluginPath = None):
		
		self._actions = ['pyplugin']
		self._objects = [self]
		self._ignoredFiles = ['__init__.py', '.DS_Store', 'desktop.ini']
		
		if pluginPath == None:
			currPath = os.path.dirname(os.path.abspath(__file__))
			self._pluginPath = os.path.join(currPath,'plugins')
		else:
			self._pluginPath = pluginPath
			
			
		initFile = os.path.join(self._pluginPath,'__init__.py')
		
		if os.path.exists(self._pluginPath):
			self.importPlugins()
		else:
			os.mkdir(self._pluginPath)
			
		if not os.path.exists(initFile):
			open(initFile,'wb').close()
			
	def importPlugins(self):

		for file in os.listdir(self._pluginPath):
			if file not in self._ignoredFiles and '.pyc' not in file:
				self.importPlugin(os.path.join(self._pluginPath, file))
				
	def importPlugin(self, pluginFile):
		
		pluginName = os.path.splitext(os.path.basename(pluginFile))[0]
		
		f, path, desc = imp.find_module(pluginName, [self._pluginPath])
		
		plugin = imp.load_module(pluginName, f, path, desc)
		
		try:
			pluginAction = getattr(sys.modules[pluginName], 'action')
			pluginObject = getattr(sys.modules[pluginName], pluginName)
		except AttributeError:
			return
		
		self._actions.append(pluginAction)
		self._objects.append(pluginObject)
		
	def getActions(self):
		return self._actions
	
	def getObjects(self):
		return self._objects
	
	def getActionsAndObjects(self):
		return zip(self._actions, self._objects)
		
	def sendInput(self, data):
		if data == 'reloadPlugins':
			self.importPlugins()
			
		return 'Reloaded plugins!'