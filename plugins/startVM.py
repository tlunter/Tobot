import subprocess

# Since this plugin starts the virtual machine you supply, startVM suits it well
action = 'startVM'

class startVM:
    
    # Every plugin must have a sendInput function that takes one variable
    # What is in the variable and what it does is up to it
    def sendInput(self, vmData):
        
        # Since the Virtual Machines can't have spaces in titles, just split the whitespace
        vmSplit = vmData.split()
        
        # The VM is most likely the first argument, so why not?
        vm = vmSplit[0]
        
        # The output will start here
        output = 'Starting {0}\n'.format(str(vm))
        
        # If the command worked correctly, print that it started
        # If it didn't return correctly, assume it's not a valid VM
        try:
            command = subprocess.check_output(['VBoxManage','startvm',str(vm),'--type','headless'],stderr=subprocess.STDOUT)
        
        except subprocess.CalledProcessError as e:
            output += '{0} is not a valid Virtual Machine'.format(str(vm))
            
        else:
            output += 'Started {0}'.format(str(vm))
        
        return output
        
# Each plugin must initialize itself at the bottom with a variable equal to the plugin name
startVM = startVM()
