from PyPlugin import PyPlugin

class Tobot:
    
    def __init__(self, name = 'Tobot'):
        
        # Initiate a PyPlugin object to gather all the plugins for Tobot
        self._plugins = PyPlugin()
        
        # Set Tobot's name
        # This will be used in select Interpreters
        self._name = name
        
    # Return the name of the bot
    def getName(self):
        return self._name
    
    # Interpret any commands given to the bot based on it's plugins
    # Plugins are called by their action keyword
    def interpret(self, username, input):
        
        # Split between the action keyword and the data to send the function
        inputSplit = input.split(None, 1)
        
        # If there is no action supplied, then nothing to return?
        try:
            action = inputSplit[0]
        except IndexError:
            return ''
        
        # Some functions might not need data, so just set it to be blank    
        try:
            data = inputSplit[1]
        except IndexError:
            data = ''
        
        # If the action is set, but not in the list, then return nothing
        output = ''
        
        # Check and see if the action exists and then call the input data function
        # This should return a string value output for the interpreter to write
        for act, obj in self._plugins.getActionsAndObjects():
            
            if action == act:
                output = obj.sendInput(data)
                
        return output
