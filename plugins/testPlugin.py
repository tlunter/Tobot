# The plugin prints your input, so print is acceptable
action = 'print'

class testPlugin:

    # Every plugin must have a sendInput function that takes one variable
    # What is in the variable and what it does is up to it
    def sendInput(self, data):
        
        # If no data is supplied, output that
        # Otherwise print out the data we gave it
        if data == '':
            return 'You didn\'t input anything'
            
        else:
            return 'You inputted: {0}'.format(data)
        
# Each plugin must initialize itself at the bottom with a variable equal to the plugin name
testPlugin = testPlugin()
