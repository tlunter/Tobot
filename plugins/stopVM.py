import subprocess

# Since this plugin stops the virtual machine you supply, stopVM suits it well
action = 'stopVM'

class stopVM:

	# Every plugin must have a sendInput function that takes one variable
	# What is in the variable and what it does is up to it
	def sendInput(self, vmData):
		
		# Since the Virtual Machines can't have spaces in titles, just split the whitespace
		vmSplit = vmData.split()
		
		# Force has to do with ACPI shutdown versus just killing the VM
		force = False
		
		# If someone specifies the force argument, remove it from the possible name and
		# Set the command to be forced
		if '--force' in vmSplit:
			vmSplit.remove('--force')
			force = True
		
		# The VM is most likely the first argument, so why not?
		vm = vmSplit[0]
		
		# The output will start here
		output = 'Stopping {0}\n'.format(str(vm))
	
		# Here we set if the command is forced or not
		if force:
			commandInput = ['VBoxManage','controlvm',str(vm),'poweroff']
			
		else:
			commandInput = ['VBoxManage','controlvm',str(vm),'acpipowerbutton']
			
		# If the command worked correctly, print that it stopped
		# If it didn't return correctly, assume it's not a valid VM
		try:
			commandOutput = subprocess.check_output(commandInput,stderr=subprocess.STDOUT)
	
		except subprocess.CalledProcessError:
			output += '{0} is not a valid Virtual Machine'.format(str(vm))
		
		else:
			output += 'Stopped {0}'.format(str(vm))
		
		return output
		
# Each plugin must initialize itself at the bottom with a variable equal to the plugin name
stopVM = stopVM()